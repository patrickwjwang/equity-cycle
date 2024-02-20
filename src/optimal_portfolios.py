import os
import warnings
import numpy as np
import pandas as pd
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns


class OptimalPortfolios:
    """
    OptimalPortfolios calculates optimal portfolio weights using the Efficient Frontier method 
    and computes portfolio returns over different time frames. 
    'Portfolio_1' is the portfolio that achieves 50-quantile stock return with minimized variance
    and 'Portfolio_num_pfo' is the 90-quantile stock return with minimized variance

    Attributes:
        stock_df (DataFrame): Historical stock prices.
        num_pfo (int): Number of portfolios on the efficient frontier.
        pfo_returns (list): List of expected returns for each portfolio.
        pfo_vars (list): List of variances for each portfolio.
    
    Example:
        stock_df = pd.read_csv('stock_data.csv')
        op = OptimalPortfolios(stock_df, num_pfo=5)
        op.calculate_efficient_frontier()
        print(op.weekly_return)
    """

    def __init__(self, stock_df, num_pfo, corr_threshold=None):
        self.stock_df = stock_df
        self.num_pfo = num_pfo

        # Automatically remove high correlation columns if threshold is provided
        if corr_threshold is not None:
            self.remove_high_corr_columns(corr_threshold)

        self._mu = expected_returns.mean_historical_return(self.stock_df)
        self._cov_matrix = risk_models.sample_cov(self.stock_df)
        self._ef = EfficientFrontier(self._mu, self._cov_matrix)
        self._ef.solver = 'Clarabel'        
        self._weights = []
        self._weights_df = None
        self._daily_return = None
        self._weekly_return = None
        self._monthly_return = None
        self._annual_return = None
        self.pfo_returns = []
        self.pfo_vars = []
    
    def calculate_efficient_frontier(self):
        pfo_mu_min = self._mu.quantile(0.5)  # 50-quantile of stock return
        pfo_mu_max = self._mu.quantile(0.9)  # 90-quantile of stock return
        return_range = np.linspace(pfo_mu_min, pfo_mu_max, self.num_pfo)

        for target_return in return_range:
            efficient_pfo = self._ef.efficient_return(target_return=target_return)
            weights_arr = np.array(list(efficient_pfo.values()))

            pfo_return = np.dot(self._mu, weights_arr)
            pfo_var = np.dot(weights_arr.T, np.dot(self._cov_matrix, weights_arr))

            self.pfo_returns.append(pfo_return)
            self.pfo_vars.append(pfo_var)
            self._weights.append(weights_arr)
        self._weights_df = pd.DataFrame(self._weights, columns=self.stock_df.columns)

    def remove_high_corr_columns(self, threshold):
        # Find indices where correlation is above the threshold
        corr_matrix = self.stock_df.corr()
        np.fill_diagonal(corr_matrix.values, np.nan)
        high_corr_pairs = np.where(np.abs(corr_matrix) >= threshold)

        # Extract the pairs and decide which column to drop
        cols_to_drop = set()
        for x, y in zip(*high_corr_pairs):
            if x != y:
                col1, col2 = self.stock_df.columns[x], self.stock_df.columns[y]
                # Add only one column from each pair, ensuring no duplicate columns are added
                cols_to_drop.add(col1)  
        
        # Drop the columns
        self.dropped_stocks = cols_to_drop
        self.stock_df = self.stock_df.drop(columns=cols_to_drop)
        self.stock_df.index = pd.to_datetime(self.stock_df.index)        
        print(f"{len(cols_to_drop)} stocks removed, {self.stock_df.shape[1]} stocks remain.")

    def get_transposed_weights_df(self):
        # Transpose the weights dataframe
        transposed_df = self._weights_df

        # Rename the columns to 'weight_1', 'weight_2', ..., 'weight_n' in one step
        column_names = {i : f'weight_{i}' for i in range(self.num_pfo)}
        transposed_df = transposed_df.rename(columns=column_names)
        
        # Rename the 'index' column to 'tickers'
        transposed_df = transposed_df.reset_index()
        transposed_df = transposed_df.rename(columns={'index': 'tickers'})
        self.weight_df = transposed_df

    def _calculate_daily_returns(self):        
        daily_returns = self.stock_df.pct_change()
        portfolio_daily_returns = np.dot(daily_returns.fillna(0), self._weights_df.T)

        # Set Date as index and name columns
        self._daily_return = pd.DataFrame(
            portfolio_daily_returns[1:],  # Skip the first row
            index=self.stock_df.index[1:],  # index skip first date
            columns=[f'portfolio_{i+1}' for i in range(self.num_pfo)])

    def _calculate_weekly_returns(self):
        weekly_returns = self.stock_df.resample('W-FRI').ffill().pct_change()
        portfolio_weekly_returns = np.dot(weekly_returns.fillna(0), self._weights_df.T)

        # Set Date as index and name columns
        self._weekly_return = pd.DataFrame(
            portfolio_weekly_returns[1:],  # Skip the first row
            index=weekly_returns.index[1:],  # index skip first date
            columns=[f'portfolio_{i+1}' for i in range(self.num_pfo)])
        
    def _calculate_monthly_returns(self):
        # Resample to get the last trading day of the month
        monthly_returns = self.stock_df.resample('M').ffill().pct_change()  
        portfolio_monthly_returns = np.dot(monthly_returns.fillna(0), self._weights_df.T)

        # Skip the first row and set Date as index and name columns
        self._monthly_return = pd.DataFrame(
            portfolio_monthly_returns[1:],  # Skip the first row
            index=monthly_returns.index[1:],  # index skip first date
            columns=[f'portfolio_{i+1}' for i in range(self.num_pfo)])

    def _calculate_annual_returns(self):
        # Resample to get the last trading day of the year
        annual_returns = self.stock_df.resample('A').ffill().pct_change()  
        portfolio_annual_returns = np.dot(annual_returns.fillna(0), self._weights_df.T)

        # Skip the first row and set Date as index and name columns
        self._annual_return = pd.DataFrame(
            portfolio_annual_returns[1:],  # Skip the first row
            index=annual_returns.index[1:],  # index skip first date
            columns=[f'portfolio_{i+1}' for i in range(self.num_pfo)])
        
    @property
    def daily_return(self):
        if self._daily_return is None:
            self._calculate_daily_returns()
        return self._daily_return

    @property
    def weekly_return(self):
        if self._weekly_return is None:
            self._calculate_weekly_returns()
        return self._weekly_return        

    @property
    def monthly_return(self):
        if self._monthly_return is None:
            self._calculate_monthly_returns()
        return self._monthly_return
    
    @property
    def annual_return(self):
        if self._annual_return is None:
            self._calculate_annual_returns()
        return self._annual_return
    
    @property
    def weight_df(self):
        if self._weights_df is None:
            warnings.warn("Efficient frontier has not been calculated. Please run calculate_efficient_frontier first.")
            return None
        else:
            # Transpose the weights dataframe
            transposed_df = self._weights_df.T

            # Rename the columns to 'weight_1', 'weight_2', ..., 'weight_n'
            column_names = {i: f'weight_{i+1}' for i in range(self.num_pfo)}
            transposed_df = transposed_df.rename(columns=column_names)
            
            # Rename the 'index' column to 'tickers' and reset index
            transposed_df = transposed_df.reset_index().rename(columns={'index': 'tickers'})            
            return transposed_df
