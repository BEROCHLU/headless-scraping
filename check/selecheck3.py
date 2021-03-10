#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if __name__ == "__main__":
    options = Options()
    prefs = {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False,
        "safebrowsing.disable_download_protection": True,
        "download.default_directory": "C:\\Users\\sadaco\\Downloads",
    }
    options.add_argument("--headless")
    options.add_argument("--window-size=1280, 1024") # fix element is not clickable at point
    options.add_experimental_option("prefs", prefs)

    ticker = "^DJI"
    url = f"https://finance.yahoo.com/quote/{ticker}/history"
    driver = webdriver.Chrome(
        executable_path="T:\\ProgramFilesT\\chromedriver_win32\\chromedriver.exe",
        chrome_options=options,
    )
    driver.implicitly_wait(16)  # 要素が見つかるまで(秒)待機 driverがcloseされない限り有効
    driver.get(url)

    try:
        elem = driver.find_element_by_css_selector(f'a[download="{ticker}.csv"]')
        if elem.is_displayed():
            elem.click()
            time.sleep(2)  # ラズパイ向けにダウンロード待ち
    except Exception as e:
        print(e)
        driver.close()
        driver.quit()
    
    driver.close()
    driver.quit()
