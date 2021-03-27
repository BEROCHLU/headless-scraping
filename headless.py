#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json
import os
import time

import pandas as pd
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if __name__ == "__main__":
    # path
    download_folder = "C:\\Users\\sadaco\\Downloads"
    download_path = os.path.join(download_folder, "t1570.csv")
    chromedriver_path = "T:/ProgramFilesT/chromedriver_win32/chromedriver.exe"
    # NK
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

    df_concat.to_csv(download_path, index=False, header=True, line_terminator="\n", encoding="utf_8_sig")
    print("Done NK")
    # DJI
    f1 = lambda n: datetime.datetime.fromtimestamp(n).strftime("%Y-%m-%d")

    ticker = "^DJI"
    strRange = "6mo"

    url_chart = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
    data_chart = requests.get(url_chart, params={"range": strRange, "interval": "1d"})
    data_chart = data_chart.json()

    hshResult = data_chart["chart"]["result"][0]
    hshQuote = hshResult["indicators"]["quote"][0]
    hshQuote["date"] = hshResult["timestamp"]

    df_quote = pd.DataFrame(hshQuote.values(), index=hshQuote.keys()).T
    df_quote = df_quote.dropna(subset=["open", "high", "low", "close"])  # OHLCに欠損値''が1つでもあれば行削除
    df_quote = df_quote.round(2)  # float64 => float32

    df_quote["date"] = df_quote["date"].map(f1)
    df_quote = df_quote.reindex(columns=["date", "open", "high", "low", "close", "volume"])

    download_path = os.path.join(download_folder, f"{ticker}.csv")
    df_quote.to_csv(download_path, index=False, header=True, line_terminator="\n")
    print("Done ^DJI")
    # selenium begin
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

    print("Done chrome-headless")
