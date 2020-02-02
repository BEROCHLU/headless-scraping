#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time

import pandas as pd
from selenium import webdriver

if __name__=='__main__':
#n225
    url = 'https://96ut.com/stock/jikei.php?code=1570'
    dfs = pd.read_html(url, header=0, index_col=0)
    df = dfs[0]
    #df = dfs[0]['初値']
    df = df.sort_values('日付')
    #print(df)

    file_path = os.environ['HOMEPATH'] + '\\Downloads\\t1570.csv'

    df.to_csv(file_path)
#sp500
    url = 'https://finance.yahoo.com/quote/UPRO/history'
    driver = webdriver.Chrome()
    driver.get(url)

    #driver.set_page_load_timeout(4) #ページがロードされるまでの待ち時間を設定する
    #driver.set_script_timeout(1) #timeoutを超えるとエラー発生
    #time.sleep(2)
    
    try:
        elem = driver.find_elements_by_css_selector('a[download="UPRO.csv"]')[0]

        if elem.is_displayed():
            elem.click()
        else:
            raise Exception
        
    except:
        print(sys.exc_info())
    finally:
        time.sleep(2)

#usd/jpy
    url = 'https://www.macrotrends.net/2550/dollar-yen-exchange-rate-historical-chart'
    #driver = webdriver.Chrome()
    driver.get(url)

    frame = driver.find_element_by_id('chart_iframe')
    driver.switch_to.frame(frame)

    try:
        elem = driver.find_element_by_id('dataDownload')
        elem.click()
    except:
        print(sys.exc_info())
    finally:
        pass
        time.sleep(2)
        driver.close()
        driver.quit()
