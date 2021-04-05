#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
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

# hash
str_k = b"aHR0cHM6Ly9rYWJ1dGFuLmpwL3N0b2NrL2thYnVrYT9jb2RlPTEzMjEmYXNoaT1kYXkmcGFnZT0="
str_s = b"aHR0cHM6Ly93d3cubWFjcm90cmVuZHMubmV0LzI1NDgvZXVyby1kb2xsYXItZXhjaGFuZ2UtcmF0ZS1oaXN0b3JpY2FsLWNoYXJ0"
str_c = b"ZXVyby1kb2xsYXItZXhjaGFuZ2UtcmF0ZS1oaXN0b3JpY2FsLWNoYXJ0LmNzdg=="
str_p = b"VDpcUHJvZ3JhbUZpbGVzVFxjaHJvbWVkcml2ZXJfd2luMzJcY2hyb21lZHJpdmVyLmV4ZQ=="
# path
chromedriver_path = base64.b64decode(str_p).decode()
download_folder = os.path.join(os.environ["USERPROFILE"], "Downloads")
output_folder = "..\\sakata\\csv"
# timezone
edt = tz.gettz("America/New_York")
# lambda
f1 = lambda dt: dt + datetime.timedelta(days=-3) if dt.weekday() == 0 else dt + datetime.timedelta(days=-1)
f2 = lambda dt: dt.strftime("%Y-%m-%d")
# filename
csv_file = base64.b64decode(str_c).decode()


def getDf_read_html():
    lst_page = []
    lst_df = None
    page = base64.b64decode(str_k).decode()

    for i in [1, 2]:
        url = f"{page}{i}"
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

    return dfHist


def getDf_eusd():
    download_path = os.path.join(download_folder, csv_file)
    df_eusd = pd.read_csv(download_path, header=None, skiprows=5706, names=["date", "close"])
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

    url = base64.b64decode(str_s).decode()
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
    df_merge.rename(columns={"始値": "open_t"}, inplace=True)

    download_path = os.path.join(output_folder, "datexyt.csv")
    df_merge.to_csv(download_path, header=False, index=False, line_terminator="\n")  # for C
    download_path = os.path.join(output_folder, "hdatexyt.csv")
    df_merge.to_csv(download_path, header=True, index=False, line_terminator="\n")  # for Python Node.js
