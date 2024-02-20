import os
import pandas as pd


# Current directory
current_dir = os.getcwd()   
tmp_data_dir = os.path.join(current_dir, 'data', 'raw', 'tmp')  # raw data directory
processed_dir = os.path.join(current_dir, 'data', 'processed')  # processed data directory



def convert_stock_price(path, convert_type, start_name):
    # Load stock price data and name first column
    df = pd.read_csv(path, dtype={0: str})
    df = df.rename(columns={df.columns[0]: 'Date'})
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Drop rows where 'Date' column is NaN    
    df.dropna(subset=['Date'], inplace=True)
    
    # Remove "US Equity" and strip white spaces from column names
    df.columns = [col.replace('US Equity', '').strip() for col in df.columns]
    
    # Find start and end dates automatically
    start_date = df['Date'].min().strftime('%y%m%d')
    end_date = df['Date'].max().strftime('%y%m%d')
    
    # Generate filename based on start and end dates and convert type
    start_date = df['Date'].min().strftime('%y%m%d')
    end_date = df['Date'].max().strftime('%y%m%d')
    filename = f"{start_name}_{start_date}_{end_date}.{convert_type}"    
    return df, filename


price_1_df, name_1 = convert_stock_price(os.path.join(tmp_data_dir, 'price_1.csv'), 'csv', 'price_1')
price_2_df, name_2 = convert_stock_price(os.path.join(tmp_data_dir, 'price_2.csv'), 'csv', 'price_2')
price_3_df, name_3 = convert_stock_price(os.path.join(tmp_data_dir, 'price_3.csv'), 'csv', 'price_3')
price_4_df, name_4 = convert_stock_price(os.path.join(tmp_data_dir, 'price_4.csv'), 'csv', 'price_4')

# Convert to csv
price_1_df.to_csv(os.path.join(processed_dir, name_1), index=False)
price_2_df.to_csv(os.path.join(processed_dir, name_2), index=False) 
price_3_df.to_csv(os.path.join(processed_dir, name_3), index=False) 
price_4_df.to_csv(os.path.join(processed_dir, name_4), index=False) 
