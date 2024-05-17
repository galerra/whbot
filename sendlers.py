from conversions import checkPhoneNumber, phoneNormalized
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

# async def sendTimeMessageToUser(userPhone, message, visit_date, visit_time: str):
#     current_time = time.localtime()
#     t = visit_time.split(":")
#     left_time = datetime.strptime(
#         f"{t[0]}:{t[1]}:0", "%H:%M:%S"
#     ) - datetime.strptime(
#         f"{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}",
#         "%H:%M:%S",
#     )
#     sleep_time = left_time.seconds - 3600
#     time.sleep(sleep_time)
#     await sendMessageToUser(userPhone, message)




        


