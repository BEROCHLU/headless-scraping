#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json
import os

import pandas as pd
import requests

# path
download_folder = "..\\sakata\\csv"
# lambda
f1 = lambda ms: datetime.datetime.fromtimestamp(ms).strftime("%Y-%m-%d")
f2 = lambda ns: datetime.datetime.fromtimestamp(ns / 1000).strftime("%Y-%m-%d")


def getDataFrame1():
    lst_page = []
    lst_df = None

    for i in [1, 2]:
        url = f"https://kabutan.jp/stock/kabuka?code=1321&ashi=day&page={i}"
        lst_df = pd.read_html(url, header=0, index_col=0)
        df_page = lst_df[5]
        lst_page.append(df_page)

    lst_df[4].index.name = "日付"
    lst_page.append(lst_df[4])

    df_concat = pd.concat(lst_page)  # page結合
    df_concat = df_concat.sort_values("日付")  # 下が最新になるようにソート

    df_concat = df_concat.reset_index()  # 日付がindexになってるので振り直し
    df_concat["日付"] = pd.to_datetime(df_concat["日付"], format="%y/%m/%d")  # フォーマット変換 yy/mm/dd => yyyy-mm-dd
    df_concat["日付"] = df_concat["日付"].dt.strftime("%Y-%m-%d")  # キャスト datetime64 to string
    # df_concat.rename(columns={'日付': 'date'}, inplace=True)
    # download_path = os.path.join(download_folder, "t1570.csv")
    # df_concat.to_csv(download_path, index=False, header=True, line_terminator="\n", encoding="utf_8_sig")
    print("Done NK")
    return df_concat


def getDataFrame2():
    ticker = "^DJI"
    strRange = "6mo"

    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
    data_chart = requests.get(url, params={"range": strRange, "interval": "1d"})
    data_chart = data_chart.json()

    hshResult = data_chart["chart"]["result"][0]
    hshQuote = hshResult["indicators"]["quote"][0]
    hshQuote["date"] = hshResult["timestamp"]

    df_quote = pd.DataFrame(hshQuote.values(), index=hshQuote.keys()).T
    df_quote = df_quote.dropna(subset=["open", "high", "low", "close"])  # OHLCに欠損値''が1つでもあれば行削除
    df_quote = df_quote.round(2)  # float64 => float32

    df_quote["date"] = df_quote["date"].map(f1)  # UNIX time to Datetime string
    df_quote = df_quote.reindex(columns=["date", "open", "high", "low", "close", "volume"])  # sort columns

    # download_path = os.path.join(download_folder, f"{ticker}.csv")
    # df_quote.to_csv(download_path, index=False, header=True, line_terminator="\n")
    print("Done ^DJI")
    return df_quote


def getDataFrame3():
    url = "https://fx.minkabu.jp/api/v2/bar/EURUSD/daily.json"
    data_eusd = requests.get(url, params={"count": 128})
    data_eusd = data_eusd.json()

    df_eusd = pd.DataFrame(data_eusd, columns=["date", "open", "high", "low", "close"])  # list to dataframe
    df_eusd["date"] = df_eusd["date"].map(f2)  # UNIX time to Datetime string
    df_eusd = df_eusd.drop(columns=["open", "high", "low"])  # いらない列削除

    # download_path = os.path.join(download_folder, "euro-dollar-exchange-rate-historical-chart.csv")
    # df_eusd.to_csv(download_path, index=False, header=True, line_terminator="\n")
    print("Done Currency")
    return df_eusd


if __name__ == "__main__":
    # vlookup
    [df_concat, df_quote, df_eusd] = [getDataFrame1(), getDataFrame2(), getDataFrame3()]

    df_merge = pd.merge(df_quote, df_eusd, on="date")
    df_merge = pd.merge(df_merge, df_concat, left_on="date", right_on="日付")
    df_merge = df_merge[["date", "close_x", "close_y", "始値"]]

    download_path = os.path.join(download_folder, "n225in.csv")
    df_merge.to_csv(download_path, header=False, index=False, line_terminator="\n")
