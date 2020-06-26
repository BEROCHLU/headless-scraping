#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import datetime
import pandas as pd
import yfinance as yf

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


if __name__ == "__main__":
    # path
    download_folder = "C:\\Users\\sadaco\\Downloads"
    download_path = os.path.join(download_folder, "t1570.csv")
    chromedriver_path = "T:\\ProgramFilesT\\chromedriver_win32\\chromedriver.exe"
    # pandas
    url = "https://96ut.com/stock/jikei.php?code=1321"
    dfs = pd.read_html(url, header=0, index_col=0)
    df = dfs[0]
    df = df.sort_values("日付")  # 下が最新になるようにソート
    df.to_csv(download_path)  # 日付がヘッダーになってないので整形するため一度出力する
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
    url = "https://www.macrotrends.net/2556/pound-japanese-yen-exchange-rate-historical-chart" #
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
        driver.close()  # エラー時、タスクが残らないように終了
        driver.quit()
    # NK225
    dt_now = datetime.datetime.now()  # 今日の日付取得
    dt_now = dt_now.strftime("%Y/%m/%d")

    dfq = df.query(f'日付 == "{dt_now}"')

    if dfq.empty:  # 今日の日付が含まれていない場合
        url = "https://stocks.finance.yahoo.co.jp/stocks/detail/?code=1321.T"
        driver.get(url)
        try:
            str_selector = "div.innerDate div.lineFi.clearfix:nth-of-type(2) dd.ymuiEditLink.mar0 > strong"
            str_open = driver.find_element_by_css_selector(str_selector).text
            str_open = str_open.replace(",", "")  # remove comma

            df = pd.read_csv(download_path)  # 出したものを読み込む
            df = df.append({"日付": dt_now, "初値": str_open}, ignore_index=True)
            df.to_csv(download_path, header=True, index=False)  # 最後に出力
        except Exception as e:  # セレクターが見つからなかった場合
            print(e)

    driver.close()
    driver.quit()

    qq = '^DJI' # CVX | ^FTSE | ^DJI
    yft = yf.Ticker(qq)

    dfHist = yft.history(period="1y")
    dfHist = dfHist.drop(columns=['Dividends', 'Stock Splits'])
    dfHist = dfHist.dropna(subset=['Open', 'High', 'Low', 'Close']) #OHLCに欠損値''が1つでもあれば行削除

    download_path = os.path.join(download_folder, f"{qq}.csv")
    dfHist.to_csv(download_path)

    print("Done chrome-headless")