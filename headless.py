#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json
import os
import time

import pandas as pd
import requests
import yfinance as yf
from dateutil import tz
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# path
download_folder = "C:\\Users\\sadaco\\Downloads"
chromedriver_path = "T:\\ProgramFilesT\\chromedriver_win32\\chromedriver.exe"
# timezone
edt = tz.gettz("America/New_York")
# lambda
f1 = lambda dt: dt + datetime.timedelta(days=-3) if dt.weekday() == 0 else dt + datetime.timedelta(days=-1)
f2 = lambda dt: dt.strftime("%Y-%m-%d")


def getDf_read_html():
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

    # download_path = os.path.join(download_folder, "t1570.csv")
    # df_concat.to_csv(download_path, index=False, header=True, line_terminator="\n", encoding="utf_8_sig")
    return df_concat


def getDf_yfinance():
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
    dfHist["date"] = dfHist["date"].dt.strftime("%Y-%m-%d")  # キャスト datetime64 to string

    # download_path = os.path.join(download_folder, f"{qq}.csv")
    # dfHist.to_csv(download_path, index=False, header=True, line_terminator="\n")
    return dfHist


def getDf_eusd():
    path_eusd = "C:\\Users\\sadaco\\Downloads\\euro-dollar-exchange-rate-historical-chart.csv"
    df_eusd = pd.read_csv(path_eusd, header=None, skiprows=5706, names=["date", "close"])
    return df_eusd


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


def deleteDownloadfile():
    csv_file = "euro-dollar-exchange-rate-historical-chart.csv"
    csv_path = os.path.join(download_folder, csv_file)

    if os.path.isfile(csv_path):
        os.remove(csv_path)
        print(f"\nremoved {csv_file}")

if __name__ == "__main__":
    seleniumDownload()
    [df_concat, df_quote, df_eusd] = [getDf_read_html(), getDf_yfinance(), getDf_eusd()]
    deleteDownloadfile()
    # vlookup
    df_merge = pd.merge(df_quote, df_eusd, on="date")
    df_merge = pd.merge(df_merge, df_concat, left_on="date", right_on="日付")
    df_merge = df_merge[["date", "close_x", "close_y", "始値"]]

    download_path = os.path.join(download_folder, "n225in.csv")
    df_merge.to_csv(download_path, header=False, index=False, line_terminator="\n")
