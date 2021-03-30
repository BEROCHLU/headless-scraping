#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json
import os
import time

import pandas as pd
import pytz
import requests
import yfinance as yf
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# path
download_folder = "C:\\Users\\sadaco\\Downloads"
chromedriver_path = "T:\\ProgramFilesT\\chromedriver_win32\\chromedriver.exe"

# lambda
f1 = lambda d: d + datetime.timedelta(days=-3) if d.weekday() == 0 else d + datetime.timedelta(days=-1)
f2 = lambda ms: datetime.datetime.fromtimestamp(ms, tz=pytz.timezone("America/New_York")).strftime("%Y-%m-%d")
f3 = lambda ns: datetime.datetime.fromtimestamp(ns / 1000).strftime("%Y-%m-%d")


def read_htmlDownload():
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

    df_concat.sort_values(by="日付", inplace=True)  # 下が最新になるようにソート
    df_concat.reset_index(inplace=True)  # 日付がindexになってるので振り直し

    df_concat["日付"] = pd.to_datetime(df_concat["日付"], format="%y/%m/%d")  # フォーマット変換 yy/mm/dd => yyyy-mm-dd
    df_concat["日付"] = df_concat["日付"].map(f1)  # 月曜日だったら先週の金曜日、それ以外は前日
    df_concat["日付"] = df_concat["日付"].dt.strftime("%Y-%m-%d")  # キャスト datetime64 to string

    download_path = os.path.join(download_folder, "t1570.csv")
    df_concat.to_csv(download_path, index=False, header=True, line_terminator="\n", encoding="utf_8_sig")


def yfinanceDownload():
    qq = "^DJI"
    yft = yf.Ticker(qq)

    dfHist = yft.history(period="6mo")
    dfHist.drop(columns=["Dividends", "Stock Splits"], inplace=True)
    dfHist.dropna(subset=["Open", "High", "Low", "Close"], inplace=True)  # OHLCに欠損値''が1つでもあれば行削除
    dfHist = dfHist.round(2)

    dfHist.reset_index(inplace=True)
    dfHist.rename(
        columns={"Date": "date", "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"},
        inplace=True,
    )

    download_path = os.path.join(download_folder, f"{qq}.csv")
    dfHist.to_csv(download_path, index=False, header=True, line_terminator="\n")


def seleniumDownload():
    options = Options()  # use chrome option
    prefs = {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False,
        "safebrowsing.disable_download_protection": True,
        "download.default_directory": download_folder,
    }
    options.add_argument("--headless")  # ヘッダレスではダウンロード指定必須
    # fix element is not clickable at point
    options.add_argument("--window-size=1280, 1024")
    options.add_experimental_option("prefs", prefs)
    # https://www.macrotrends.net/2556/pound-japanese-yen-exchange-rate-historical-chart | https://www.macrotrends.net/2550/dollar-yen-exchange-rate-historical-chart
    url = "https://www.macrotrends.net/2548/euro-dollar-exchange-rate-historical-chart"
    driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=options)
    driver.implicitly_wait(16)  # 要素が見つかるまで(秒)待機 driverがcloseされない限り有効
    driver.get(url)

    frame = driver.find_element_by_id("chart_iframe")
    driver.switch_to.frame(frame)  # iframeにスイッチ

    try:
        elem = driver.find_element_by_id("dataDownload")
        if elem.is_displayed():
            elem.click()
            time.sleep(2)  # ラズパイ向けにダウンロード待ち
    except Exception as e:
        print(e)
    finally:
        driver.close()  # 正常及び異常時、タスクが残らないように終了
        driver.quit()


if __name__ == "__main__":
    read_htmlDownload()
    yfinanceDownload()
    seleniumDownload()