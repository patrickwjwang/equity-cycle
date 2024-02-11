import numpy as np
import pandas as pd
import os

# Current directory
current_dir = os.getcwd()   
raw_data_dir = os.path.join(current_dir, 'data', 'raw')  # raw data directory
processed_path = os.path.join(current_dir, 'data', 'processed')  # processed data directory

# File path for data from French's data library
mom_file = os.path.join(raw_data_dir, 'F-F_Momentum_Factor.CSV')  
mom_daily_file = os.path.join(raw_data_dir, 'F-F_Momentum_Factor_daily.CSV')  
ff5_file = os.path.join(raw_data_dir, 'F-F_Research_Data_5_Factors_2x3.csv')  
ff5_daily_file = os.path.join(raw_data_dir, 'F-F_Research_Data_5_Factors_2x3_daily.CSV')  

# Load momentum file and replace NA values
mom_df = pd.read_csv(mom_file, skiprows=13)  # 13 rows of descriptive headers
mom_df.columns = ['time', 'MOM']  # set column names
mom_df['time'] = mom_df['time'].astype(str).fillna('')  # fill na time with empty space
mom_df.replace([-99.99, -999], np.inf, inplace=True)  # replace French's NA values with inf

# Seperate annual and monthly data
annual_start_index = mom_df[mom_df['time'].str.contains("January-December")].index[0]
mom_year_df = mom_df[annual_start_index+2:-1].reset_index(drop=True)
mom_month_df = mom_df[:annual_start_index-1]

# Load ff5 file and replace NA values
ff5_df = pd.read_csv(ff5_file, skiprows=3)  # 3 rows of descriptive headers
ff5_df.columns = ['time', 'Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'RF']  # set column names
ff5_df['time'] = ff5_df['time'].astype(str).fillna('')  # fill na time with empty space

# Seperate annual and monthly data
annual_start_index_ff5 = ff5_df[ff5_df['time'].str.contains("January-December")].index[0]
ff5_year_df = ff5_df[annual_start_index_ff5+2:].reset_index(drop=True)
ff5_month_df = ff5_df[:annual_start_index_ff5]

# Combine annual df for mom and ff5
ff6_year_df = pd.merge(mom_year_df, ff5_year_df, on='time', how='inner')
ff6_year_df.rename(columns={'time': 'Year'}, inplace=True)
# ff6_year_df.to_csv(os.path.join(processed_path, 'ff6_yearly.csv'), index=False)  # save ff6_year_df to csv

# Combine monthly df for mom and ff5
ff6_month_df = pd.merge(ff5_month_df, mom_month_df, on='time', how='inner')
ff6_month_df.rename(columns={'time': 'Year_Month'}, inplace=True)
ff6_month_df['Year_Month'] = pd.to_datetime(ff6_month_df['Year_Month'], format='%Y%m').dt.to_period('M')
ff6_month_df = ff6_month_df[ff6_month_df['Year_Month'].dt.year >= 1964]  # filter after 1964 since 1963 incomplete
# ff6_month_df.to_csv(os.path.join(processed_path, 'ff6_monthly.csv'), index=False)  # save ff6_month_df to csv

"""
# Check mom annual and month data
mom_year_df.head()  # 1927
mom_year_df.tail()  # 2023
print(len(mom_year_df))  # 97
mom_month_df.head()  # 192701
mom_month_df.tail()  # 202312
print(len(mom_month_df))  # 1164

# Check ff5 annual and month data
ff5_year_df.head()  # 1964
ff5_year_df.tail()  # 2023
print(len(ff5_year_df))  # 60
ff5_month_df.head()  # 196307
ff5_month_df.tail()  # 202312
print(len(ff5_month_df))  # 726

# Check the combined ff6 df yearly 
print(ff6_year_df.head())  # 1964
print(ff6_year_df.tail())  # 2023
print(len(ff6_year_df))  # 60

# Check the combined ff6 df monthly df
print(ff6_month_df.head())  # 1964-01
print(ff6_month_df.tail())  # 2023-12
print(len(ff6_month_df))  # 720
"""

# Load momentum daily file
mom_daily_df = pd.read_csv(mom_daily_file, skiprows=13)  # 13 rows of descriptive headers
mom_daily_df = mom_daily_df.drop(mom_daily_df.tail(1).index)  # some useless metadata
mom_daily_df.columns = ['Date', 'MOM']  # set column names
mom_daily_df['Date'] = pd.to_datetime(mom_daily_df['Date'], format='%Y%m%d')

# Load ff5 daily file
ff5_daily_df = pd.read_csv(ff5_daily_file, skiprows=3)  # 13 rows of descriptive headers
ff5_daily_df.columns = ['Date', 'Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'RF']  # set column names
ff5_daily_df['Date'] = pd.to_datetime(ff5_daily_df['Date'], format='%Y%m%d')

# Combine ff5 and momentum daily df
ff6_daily_df = pd.merge(mom_daily_df, ff5_daily_df, on='Date', how='inner')
ff6_daily_df = ff6_daily_df[ff6_daily_df['Date'].dt.year >= 1964]  # filter after 1964 since 1963 incomplete
# ff6_daily_df.to_csv(os.path.join(processed_path, 'ff6_daily.csv'), index=False)  # Save ff6_daily_df to csv

"""
# Check mom daily df
mom_daily_df.head()  # 19261103
mom_daily_df.tail()  # 20231229
print(len(mom_daily_df))  # 25548
print(mom_daily_df.describe())

# Check ff5 daily df
ff5_daily_df.head()   # 19630701
ff5_daily_df.tail()   # 20231229
print(len(ff5_daily_df))  # 15229
print(ff5_daily_df.describe())

# Check combined daily df
print(ff6_daily_df.head())  # 1964-01-02
print(ff6_daily_df.tail())  # 2023-12-29
print(len(ff6_daily_df))  # 15103
"""

# Calculate the compound weekly return (this is not entirely accurate)
def compound_returns(x):
    return (np.prod(1 + x) - 1) * 100
ff6_daily_tmp = ff6_daily_df.copy()
ff6_daily_tmp['Week'] = ff6_daily_df['Date'].dt.isocalendar().week  # create a column for week
ff6_daily_tmp['Year'] = ff6_daily_df['Date'].dt.year  # create a column for year
ff6_daily_tmp2 = ff6_daily_tmp.drop(columns=['Date'])
ff6_daily_tmp2[ff6_daily_tmp2.columns.difference(['Year', 'Week'])] /= 100  # convert returns to decimal
ff6_week_df = ff6_daily_tmp2.groupby(['Year', 'Week']).apply(compound_returns).drop(columns=['Week', 'Year'])
ff6_week_df = ff6_week_df.reset_index()

# Add the last day of the week back to ff6 weekly df
last_day_of_week = ff6_daily_tmp.groupby(['Year', 'Week'])['Date'].max().reset_index()
ff6_week_df = pd.merge(ff6_week_df, last_day_of_week, on=['Year', 'Week'], how='left')
ff6_week_df = ff6_week_df.drop(columns=['Year', 'Week'])
columns_order = ['Date'] + [col for col in ff6_week_df.columns if col not in ['Date']]
ff6_week_df = ff6_week_df[columns_order]
# ff6_week_df.to_csv(os.path.join(processed_path, 'ff6_weekly.csv'), index=False)  # Save ff6_week_df to csv

"""
print(ff6_week_df.head())  # 1964-01-03 (FRI)
print(ff6_week_df.tail())  # 2023-12-29 (FRI)
print(len(ff6_week_df))    # 3131
"""

# Load HXZ factors
hxz_yearly_file = os.path.join(raw_data_dir, 'q5_factors_annual_2022.csv')
hxz_monthly_file = os.path.join(raw_data_dir, 'q5_factors_monthly_2022.csv')
hxz_weekly_file = os.path.join(raw_data_dir, 'q5_factors_weekly_2022.csv')
hxz_daily_file = os.path.join(raw_data_dir, 'q5_factors_daily_2022.csv')

# Load HXZ yearly df
hxz_yearly_df = pd.read_csv(hxz_yearly_file)
hxz_yearly_df.columns = ['Year', 'RF_HXZ', 'Mkt-RF_HXZ', 'ME_HXZ', 'IA_HXZ', 'ROE_HXZ', 'EG_HXZ']
# hxz_yearly_df.to_csv(os.path.join(processed_path, 'hxz_yearly.csv'), index=False)   # Save HXZ yearly df to csv

# Load HXZ monthly df
hxz_monthly_df = pd.read_csv(hxz_monthly_file)
hxz_monthly_df.columns = ['Year', 'Month', 'RF_HXZ', 'Mkt-RF_HXZ', 'ME_HXZ', 'IA_HXZ', 'ROE_HXZ', 'EG_HXZ']

# Create a 'Year_Month' column
hxz_monthly_df['Year_Month'] = pd.to_datetime(hxz_monthly_df['Year'].astype(str) + hxz_monthly_df['Month'].astype(str).str.zfill(2), format='%Y%m')
hxz_monthly_df['Year_Month'] = hxz_monthly_df['Year_Month'].dt.to_period('M')
columns = list(hxz_monthly_df.columns)  # Rearrange columns to put 'Year_Month' after 'Month'
year_month_index = columns.index('Year_Month')
columns.insert(2, columns.pop(year_month_index))
hxz_monthly_df = hxz_monthly_df[columns]
hxz_monthly_df = hxz_monthly_df.drop(columns=['Year', 'Month'])
# hxz_monthly_df.to_csv(os.path.join(processed_path, 'hxz_monthly.csv'), index=False)   # Save HXZ monthly df to csv

# Load HXZ weekly df
hxz_weekly_df = pd.read_csv(hxz_weekly_file)
hxz_weekly_df.columns = ['Date', 'RF_HXZ', 'Mkt-RF_HXZ', 'ME_HXZ', 'IA_HXZ', 'ROE_HXZ', 'EG_HXZ']
hxz_weekly_df['Date'] = pd.to_datetime(hxz_weekly_df['Date'], format='%Y%m%d')
# hxz_weekly_df.to_csv(os.path.join(processed_path, 'hxz_weekly.csv'), index=False)   # Save HXZ weekly df to csv

# Load HXZ daily df
hxz_daily_df = pd.read_csv(hxz_daily_file)
hxz_daily_df.columns = ['Date', 'RF_HXZ', 'Mkt-RF_HXZ', 'ME_HXZ', 'IA_HXZ', 'ROE_HXZ', 'EG_HXZ']
hxz_daily_df['Date'] = pd.to_datetime(hxz_daily_df['Date'], format='%Y%m%d')
# hxz_daily_df.to_csv(os.path.join(processed_path, 'hxz_daily.csv'), index=False)   # Save HXZ daily df to csv

"""
# Check HXZ yearly df
print(hxz_yearly_df.head())  # 1967
print(hxz_yearly_df.tail())  # 2022
print(len(hxz_yearly_df))    # 56

# Check HXZ monthly df
print(hxz_monthly_df.head())  # 1967-01
print(hxz_monthly_df.tail())  # 2022-12
print(len(hxz_monthly_df))    # 672

# Check HXZ weekly df
print(hxz_weekly_df.head())  # 1967-01-06
print(hxz_weekly_df.tail())  # 2022-12-30
print(len(hxz_weekly_df))    # 2922

# Check HXZ daily df
print(hxz_daily_df.head())  # 1967-01-03
print(hxz_daily_df.tail())  # 2022-12-30
print(len(hxz_daily_df))    # 14096
"""
