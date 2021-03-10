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
    options.add_experimental_option("prefs", prefs)

    url = "https://stocks.finance.yahoo.co.jp/stocks/detail/?code=1321.T"
    driver = webdriver.Chrome(
        executable_path="T:\\ProgramFilesT\\chromedriver_win32\\chromedriver.exe",
        chrome_options=options,
    )
    driver.get(url)

    try:
        str_open = driver.find_element_by_css_selector(
            "div.innerDate div.lineFi.clearfix:nth-of-type(2) dd.ymuiEditLink.mar0 > strong"
        ).text
        str_open = str_open.replace(",", "")
        print(str_open)
    except Exception as e:
        print(e)
        driver.close()
        driver.quit()
    finally:
        driver.close()
        driver.quit()
