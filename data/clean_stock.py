import os
import pandas as pd
import numpy as np


# Current directory
current_dir = os.getcwd()   
tmp_data_dir = os.path.join(current_dir, 'data', 'raw', 'tmp')  # raw data directory
processed_dir = os.path.join(current_dir, 'data', 'processed')  # processed data directory

def convert_stock_price(path):
    # Load stock price data, setting all columns to string type initially
    df = pd.read_csv(path, dtype=str)

    # Rename the first column to 'Date' and convert to datetime
    df = df.rename(columns={df.columns[0]: 'Date'})
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Drop rows where 'Date' column is NaN
    df.dropna(subset=['Date'], inplace=True)
    
    # Remove "US Equity" and strip white spaces from column names
    df.columns = [col.replace('US Equity', '').strip() for col in df.columns]

    # Convert all columns except 'Date' to float using vectorized operation, convert errors to NaN
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

    return df


stock_price_names = ['price_1.csv', 'price_2.csv', 'price_3.csv', 'price_4.csv']
for idx, f in enumerate(stock_price_names):
    price_df = convert_stock_price(os.path.join(tmp_data_dir, f))
    # price_df.to_csv(os.path.join(processed_dir, f), index=False)
    start, end = price_df['Date'].min(), price_df['Date'].max()
    num_columns = price_df.shape[1]  # Number of columns
    print(f"Cycle {idx+1} starts from {start}, ends with {end}, and has {num_columns} stocks.")
    
liquidity_names = ['turnover_1.csv', 'turnover_2.csv', 'turnover_3.csv', 'turnover_4.csv']
for idx, f in enumerate(liquidity_names):
    price_df = convert_stock_price(os.path.join(tmp_data_dir, f))
    price_df.to_csv(os.path.join(processed_dir, f), index=False)
    start, end = price_df['Date'].min(), price_df['Date'].max()
    num_columns = price_df.shape[1]  # Number of columns
    print(f"Cycle {idx+1} starts from {start}, ends with {end}, and has {num_columns} stocks.")

credit_names = ['credit_risk_1.csv', 'credit_risk_2.csv', 'credit_risk_3.csv', 'credit_risk_4.csv']
for idx, f in enumerate(credit_names):
    df = convert_stock_price(os.path.join(tmp_data_dir, f))
    df.to_csv(os.path.join(processed_dir, f), index=False)
    start, end = df['Date'].min(), df['Date'].max()
    num_columns = df.shape[1]  # Number of columns
    print(f"Cycle {idx+1} starts from {start}, ends with {end}, and has {num_columns} stocks.")