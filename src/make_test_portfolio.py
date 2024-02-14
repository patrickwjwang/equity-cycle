import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import plotting
from scipy.interpolate import make_interp_spline

# NOT OPTIMIZED CODE
# To do: convert the for loop into the following class
"""
class ef(num_pfo, stock_df):
    stock_df contains daily stock price data for n stocks and m days
    
    def __init__:
        ef.stock_return  # one dimension array that contain individual stock annualized return
        ef.cov_matrix  # two dimension array that contain the variance-covariance matrix of stocks        
        ef.pfo_returns  # one dimension array that contain returns on ef frontier
        ef.pfo_vars  # one dimension array that contain variances on ef frontier
        ef.weights  # two dimensional df (num_pfo by n) array that contain optimal portfolio weights
        ef.daily_return  # df (num_pfo by m) that contain optimal portfolio daily returns
        ef.weekly_return  # df (num_pfo by approx(m/5)) that contain optimal portfolio weekly return
"""

# Ignore FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Get directories 
current_dir = os.getcwd()   
processed_dir = os.path.join(current_dir, 'data', 'processed')  # processed data directory
graphs_dir = os.path.join(current_dir, 'results', 'graphs')  # graphs directory

# Read sp1500 data
df = pd.read_parquet(os.path.join(processed_dir, 'sp1500_199603_200111.parquet'))

# Expected annual returns
mu = expected_returns.mean_historical_return(df)
cov_matrix = risk_models.sample_cov(df)
ef = EfficientFrontier(mu, cov_matrix)
ef.solver = 'Clarabel'

# Set our desire portfolio return
pfo_num = 20
pfo_mu_min = mu.quantile(0.5)  # 50-quantile of stock return
pfo_mu_max = mu.quantile(0.9)  # 90-quantile of stock return
return_range = np.linspace(pfo_mu_min, pfo_mu_max, pfo_num)

# Calculate efficient portfolios given return
pfo_returns, pfo_vars = [], []
for i, target_return in enumerate(return_range):  
    # Optimize portfolio for the target return  
    efficient_pfo = ef.efficient_return(target_return=target_return)
    weights_arr = np.array(list(efficient_pfo.values()))    
    
    # Calculate expected portfolio return and variance
    pfo_return = np.dot(mu, np.array(list(weights_arr)))        
    pfo_var = np.dot(weights_arr.T, np.dot(cov_matrix, weights_arr))    
    pfo_returns.append(pfo_return)
    pfo_vars.append(pfo_var)
    
    # Print the result
    print(f"Portfolio {i+1} complete; return: {round(pfo_return, 4)}, variance: {round(pfo_var, 4)}.")

    # Check if return is close to target return (with some tolerance)
    if not np.isclose(pfo_return, target_return, atol=1e-4):
        print(f"Portfolio {i+1} expected return {pfo_return} differs from the target return {target_return}")





# Convert lists to numpy arrays for easier manipulation
pfo_returns_array = np.array(pfo_returns)
pfo_vars_array = np.array(pfo_vars)
sorted_indices = np.argsort(pfo_vars_array)
pfo_vars_sorted = pfo_vars_array[sorted_indices]
pfo_returns_sorted = pfo_returns_array[sorted_indices]

# Creating the spline
spline = make_interp_spline(pfo_vars_sorted, pfo_returns_sorted, k=3)  # k is the degree of the spline
smooth_vars = np.linspace(pfo_vars_sorted.min(), pfo_vars_sorted.max(), 300)
smooth_returns = spline(smooth_vars)

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(pfo_vars, pfo_returns, color='royalblue', label='Portfolios')
plt.plot(smooth_vars, smooth_returns, color='royalblue', label='Efficient Frontier')
plt.title('Efficient Frontier from SP1500 (1996/03 - 2001/11)')
plt.xlabel('Variance (Risk)')
plt.ylabel('Expected Return')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(graphs_dir, 'sp1500sample_efficient_frontier.png'), dpi=300) 
