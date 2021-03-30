#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json
import os

import pandas as pd
import requests
import pytz

# path
download_folder = "..\\sakata\\csv"
# lambda
f1 = lambda d: d + datetime.timedelta(days=-3) if d.weekday() == 0 else d + datetime.timedelta(days=-1)
f2 = lambda ms: datetime.datetime.fromtimestamp(ms, tz=pytz.timezone("America/New_York")).strftime("%Y-%m-%d")
f3 = lambda ns: datetime.datetime.fromtimestamp(ns / 1000).strftime("%Y-%m-%d")


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
    df_concat["日付"] = df_concat["日付"].map(f1)  # 月曜日だったら先週の金曜日、それ以外は前日
    df_concat["日付"] = df_concat["日付"].dt.strftime("%Y-%m-%d")  # キャスト datetime64 to string
    
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

    df_quote["date"] = df_quote["date"].map(f2)  # UNIX time to EDT Datetime string
    df_quote = df_quote.reindex(columns=["date", "open", "high", "low", "close", "volume"])  # sort columns

    print("Done ^DJI")
    return df_quote


def getDataFrame3():
    url = "https://fx.minkabu.jp/api/v2/bar/EURUSD/daily.json"
    data_eusd = requests.get(url, params={"count": 128})
    data_eusd = data_eusd.json()

    df_eusd = pd.DataFrame(data_eusd, columns=["date", "open", "high", "low", "close"])  # list to dataframe
    df_eusd["date"] = df_eusd["date"].map(f3)  # UNIX time to JST Datetime string
    df_eusd = df_eusd.drop(columns=["open", "high", "low"])  # いらない列削除

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
