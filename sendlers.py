from conversions import phoneNormalized
from whatsappActions import chromeSetup, openWhatsapp, clickOnSendButtom
import time
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime

def sendMessageToUser(userPhone, message):
    userPhone = phoneNormalized(userPhone)
    driver = chromeSetup()
    wait = WebDriverWait(driver, 30)
    openWhatsapp(userPhone, message, driver)
    clickOnSendButtom(driver, wait)
    time.sleep(5)






        


