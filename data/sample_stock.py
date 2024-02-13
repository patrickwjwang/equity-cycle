import bs4 as bs
import requests
import yfinance as yf
import json
import os
import pandas as pd


# Get directories 
current_dir = os.getcwd()   
processed_dir = os.path.join(current_dir, 'data', 'processed')  # processed data directory


def get_sp_tickers(num):
    wiki_url = 'http://en.wikipedia.org/wiki/List_of_S%26P_' + str(num) + '_companies'
    resp = requests.get(wiki_url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
    tickers = [s.replace('\n', '') for s in tickers]
    return tickers

"""
sp500_tickers = get_sp_tickers(500)  # S&P 500 Tickers
sp400_tickers = get_sp_tickers(400)  # S&P MidCap 400 Tickers
sp600_tickers = get_sp_tickers(600)  # S&P SmallCap 600 Tickers

# Convert the tickers to a JSON string
all_tickers = {'SP500': sp500_tickers, 'SP400': sp400_tickers, 'SP600': sp600_tickers}
json_data = json.dumps(all_tickers, indent=4)
with open(os.path.join(processed_dir, 'sp_tickers.json'), 'w') as file:
    file.write(json_data)
"""


def get_stock_data(tickers, category, start_date, end_date):
    """
    tickers: list of tickers
    category: price category. E.g. 'Close', 'Adj Close'.
    start_date, end_date: start and end date. E.g. 1996-03-01
    """
    df = yf.download(tickers, start=start_date, end=end_date, group_by='Ticker')
    df = df.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index(level=1)
    pivoted_df = df.pivot(columns='Ticker', values=category).dropna(axis=1)
    return pivoted_df

"""
# Extract the s&p tickers from json
with open(os.path.join(processed_dir, 'sp_tickers.json'), 'r') as file:
    tickers_data = file.read()
all_tickers = json.loads(tickers_data)

# Download the stock data for all tickers in SP1500 
start_date = '1996-03-01'  # start date
end_date = '2001-11-30'    # end date
sp500_df = get_stock_data(all_tickers['SP500'], 'Adj Close', start_date, end_date)
sp400_df = get_stock_data(all_tickers['SP400'], 'Adj Close', start_date, end_date)
sp600_df = get_stock_data(all_tickers['SP600'], 'Adj Close', start_date, end_date)
sp_combined_df = pd.concat([sp500_df, sp400_df, sp600_df], axis=1)

# Store it to parquet instead of csv to save space
sp_combined_df.to_parquet(os.path.join(processed_dir, 'sp1500_199603_200111.parquet')) 
"""
