import os
import pandas as pd
import matplotlib.pyplot as plt

# Directory
current_dir = os.getcwd()   
data_dir = os.path.join(current_dir, 'data', 'processed')  # processed data directory
tables_dir = os.path.join(current_dir, 'results', 'tables')  # tables directory
graphs_dir = os.path.join(current_dir, 'results', 'graphs')  # graphs directory

# Read processed files
ff6_weekly_df = pd.read_csv(os.path.join(data_dir, 'ff6_weekly.csv'))
ff6_monthly_df = pd.read_csv(os.path.join(data_dir, 'ff6_monthly.csv'))
hxz_weekly_df = pd.read_csv(os.path.join(data_dir, 'hxz_weekly.csv'))
hxz_monthly_df = pd.read_csv(os.path.join(data_dir, 'hxz_monthly.csv'))

# Create summmary stat for weekly ff6 and output to latex table (txt)
ff6_weekly_summary = ff6_weekly_df.describe()
start, end = min(ff6_weekly_df['Date']), max(ff6_weekly_df['Date'])  # start and end date
ff6_weekly_summary_latex = ff6_weekly_summary.to_latex(
    float_format = "%.2f", 
    escape = 'latex', 
    caption = f"FF5 and Momentum Factors ({start} to {end}, weekly return \%)",
    label = "tab:ff6_summary")
ff6_weekly_summary_latex = ff6_weekly_summary_latex.replace("\\begin{table}", "\\begin{table}\n\\centering")

# Sore the table in txt format
with open(os.path.join(tables_dir, 'ff6_weekly_summary.txt'), 'w') as file:
    file.write(ff6_weekly_summary_latex)

# Create summmary stat for weekly HXZ and output to latex table (txt)
hxz_weekly_summary = hxz_weekly_df.describe()
start, end = min(hxz_weekly_df['Date']), max(hxz_weekly_df['Date'])  # start and end date
hxz_weekly_summary_latex = hxz_weekly_summary.to_latex(
    float_format = "%.2f", 
    escape = 'latex', 
    caption = f"HXZ Factors ({start} to {end}, weekly return \%)",
    label = "tab:hxz_summary")
hxz_weekly_summary_latex = hxz_weekly_summary_latex.replace("\\begin{table}", "\\begin{table}\n\\centering")

# Sore the table in txt format
with open(os.path.join(graphs_dir, 'hxz_weekly_summary.txt'), 'w') as file:
    file.write(hxz_weekly_summary_latex)


# Line chart for ff6 monthly
ff6_monthly_df['Year_Month'] = pd.to_datetime(ff6_monthly_df.index)
variables = ['MOM', 'Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']  # excluding 'RF'

# Create a 2x3 subplot
fig, axs = plt.subplots(2, 3, figsize=(15, 10))
axs = axs.flatten()
for i, var in enumerate(variables):
    axs[i].plot(ff6_monthly_df['Year_Month'], ff6_monthly_df[var])
    axs[i].set_title(var)
    axs[i].set_xlabel('Date')
    axs[i].set_ylabel('Values')
plt.tight_layout()
plt.savefig(os.path.join(graphs_dir, 'ff6_monthly_plots.png'))


# Line chart for hxz monthly
hxz_monthly_df['Year_Month'] = pd.to_datetime(hxz_monthly_df['Year_Month'])
variables = ['RF_HXZ', 'Mkt-RF_HXZ', 'ME_HXZ', 'IA_HXZ', 'ROE_HXZ', 'EG_HXZ']

# Create a 2x3 subplot
fig, axs = plt.subplots(2, 3, figsize=(15, 10))
axs = axs.flatten()
for i, var in enumerate(variables):
    axs[i].plot(hxz_monthly_df['Year_Month'], hxz_monthly_df[var])
    axs[i].set_title(var)
    axs[i].set_xlabel('Date')
    axs[i].set_ylabel('Values')
plt.tight_layout()
plt.savefig(os.path.join(graphs_dir, 'hxz_monthly_plots.png'))
