#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import df2csv
import openpycel

if __name__=='__main__':
#remove download files
    try:
        os.remove('C:\\Users\\sadaco\\Downloads\\t1570.csv')
        os.remove('C:\\Users\\sadaco\\Downloads\\dollar-yen-exchange-rate-historical-chart.csv')
        os.remove('C:\\Users\\sadaco\\Downloads\\UPRO.csv')
    except Exception as e:
        pass #do nothing
#t1570
    url = 'https://96ut.com/stock/jikei.php?code=1570'
    dfs = pd.read_html(url, header=0, index_col=0)
    df = dfs[0]
    df = df.sort_values('日付') #下が最新になるようにソート
    df.to_csv('C:\\Users\\sadaco\\Downloads\\t1570.csv')
#fxy
    options = Options() #use chrome option
    prefs = {'download.prompt_for_download': False,
         'download.directory_upgrade': True,
         'safebrowsing.enabled': False,
         'safebrowsing.disable_download_protection': True,
         'download.default_directory' : 'C:\\Users\\sadaco\\Downloads'}
    options.add_argument('--headless') #ヘッダレスではダウンロード指定必須
    options.add_experimental_option('prefs', prefs)

    url = 'https://www.macrotrends.net/2550/dollar-yen-exchange-rate-historical-chart'
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)

    frame = driver.find_element_by_id('chart_iframe')
    driver.switch_to.frame(frame) #iframeにスイッチ

    try:
        driver.implicitly_wait(4) #連続して使う場合はどういう扱いになるのか
        elem = driver.find_element_by_id('dataDownload')

        if elem.is_displayed():
            elem.click()
            time.sleep(2) #ラズパイ向けに待ち
    except Exception as e:
        print(e)
        driver.close() #エラー時、タスクが残らないように終了
        driver.quit()
#upro
    url = 'https://finance.yahoo.com/quote/UPRO/history'
    driver.get(url)

    #driver.set_page_load_timeout(4) #ページがロードされるまでの待ち時間を設定する
    #driver.set_script_timeout(1) #timeoutを超えるとエラー発生
    
    try:
        driver.implicitly_wait(4) #次の要素が見つかるまで(秒)待機
        elem = driver.find_element_by_css_selector('a[download="UPRO.csv"]')

        if elem.is_displayed():
            elem.click()
            time.sleep(2) #ラズパイ向けに待ち
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()
        print('Done scrake96')
#excel
    openpycel.openpycel()
    df2csv.df2csv()
