#! /usr/bin/python
# coding: UTF-8

import pandas as pd

url = 'https://finance.yahoo.com/quote/SPY/history'
dfs = pd.read_html(url, header=0, index_col=0)
df = dfs[0]#[['Date', 'Open','High', 'Low', 'Close*']]
print(df)
#print(dfs[0][['Date', 'Open','High', 'Low', 'Close*']])
df.to_csv('SPY.csv')
