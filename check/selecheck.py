from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if __name__=='__main__':
    options = Options()
    prefs = {'download.prompt_for_download': False,
         'download.directory_upgrade': True,
         'safebrowsing.enabled': False,
         'safebrowsing.disable_download_protection': True,
         'download.default_directory' : 'C:\\Users\\sadaco\\Downloads'}
    options.add_argument('--headless')
    options.add_experimental_option('prefs', prefs)

    url = 'https://www.macrotrends.net/2550/dollar-yen-exchange-rate-historical-chart'
    driver = webdriver.Chrome(executable_path="T:\\ProgramFilesT\\chromedriver_win32\\chromedriver.exe", chrome_options=options)
    driver.get(url)

    frame = driver.find_element_by_id('chart_iframe')
    driver.switch_to.frame(frame) #iframeにスイッチ

    try:
        driver.implicitly_wait(4)
        elem = driver.find_element_by_id('dataDownload')

        if elem.is_displayed():
            elem.click()
    except Exception as e:
        print(e)
        driver.close()
        driver.quit()
    finally:
        driver.close()
        driver.quit()