from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from conversions import linkProcessing
from webdriver_manager.core.os_manager import ChromeType
import undetected_chromedriver as driver
import time


def openWhatsapp(userPhone, message, driver):
    driver.get(linkProcessing(userPhone, message))

def chromeSetup():
    service = Service(executable_path='/usr/local/bin/chromedriver-linux64')
    #options = webdriver.FirefoxOptions()
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--allow-profiles-outside-user-dir')
    options.add_argument('--enable-profile-shortcut-manager')
    options.add_argument( r'user-data-dir=C:\Users\Lenovo\Desktop\whbot\sel')                                 # УКАЖИТЕ ПУТЬ ГДЕ ЛЕЖИТ ВАШ ФАЙЛ. Советую создать отдельную папку.
    options.add_argument('--profile-directory=Profile 1')
    options.add_argument('--profiling-flush=n')
    options.add_argument('--enable-aggressive-domstorage-flushing')
    driver = webdriver.Chrome(service = service, options=options)
    # driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    return driver


def clickOnSendButtom(driver, wait):
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                           "#main > footer > div._ak1k.xnpuxes.copyable-area > div > span:nth-child(2) > div > div._ak1r > div._ak1t._ak1u > button > span")))
    driver.find_element(By.CSS_SELECTOR,
                        "#main > footer > div._ak1k.xnpuxes.copyable-area > div > span:nth-child(2) > div > div._ak1r > div._ak1t._ak1u > button > span").click()


def holdingWhatsapp(wait):
    driver = chromeSetup()
    openWhatsapp("", "", driver)
    time.sleep(20)
    driver.save_screenshot('wh.png')
    time.sleep(20)
    driver.save_screenshot('wh.png')
    time.sleep(20)
    time.sleep(wait)





