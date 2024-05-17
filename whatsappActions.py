from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from conversions import linkProcessing

# def clickOnTextBox():
#     pg.moveTo(getScreenSize()["width"] * 0.694, getScreenSize()["height"] * 0.964)  # Moves the cursor the the message bar in Whatsapp
#     pg.click()

def openWhatsapp(userPhone, message, driver):
    driver.get(linkProcessing(userPhone, message))

# def closeWhatsapp():
#     _system = system().lower()
#     if _system in ("windows", "linux"):
#         pg.hotkey("ctrl", "w")
#     elif _system == "darwin":
#         pg.hotkey("command", "w")
#     else:
#         raise Warning(f"{_system} not supported!")
#     pg.press("enter")

def chromeSetup():
    options = webdriver.ChromeOptions()
    options.add_argument('--allow-profiles-outside-user-dir')
    options.add_argument('--enable-profile-shortcut-manager')
    options.add_argument( r'user-data-dir=C:\Users\Lenovo\Desktop\whbot\sel')  # УКАЖИТЕ ПУТЬ ГДЕ ЛЕЖИТ ВАШ ФАЙЛ. Советую создать отдельную папку.
    options.add_argument('--profile-directory=Profile 1')
    options.add_argument('--profiling-flush=n')
    options.add_argument('--enable-aggressive-domstorage-flushing')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def clickOnSendButtom(driver, wait):
    # wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
    #                                        "#main > footer > div._2lSWV._3cjY2.copyable-area > div > span:nth-child(2) > div > div._1VZX7 > div._2xy_p._3XKXx > button > span")))
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                           "#main > footer > div._ak1k._ahmw.copyable-area > div > span:nth-child(2) > div > div._ak1r > div._ak1t._ak1u > button > span")))
    # driver.find_element(By.CSS_SELECTOR,
    #                     "#main > footer > div._2lSWV._3cjY2.copyable-area > div > span:nth-child(2) > div > div._1VZX7 > div._2xy_p._3XKXx > button > span").click()
    driver.find_element(By.CSS_SELECTOR,
                            "#main > footer > div._ak1k._ahmw.copyable-area > div > span:nth-child(2) > div > div._ak1r > div._ak1t._ak1u > button").click()