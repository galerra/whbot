# # import pywhatkit
# # import keyboard as k
# # import time
# # import pyautogui
# # from tkinter import *
# # import os
# # from platform import system
# #
# # def getScreenSize():
# #     win = Tk()
# #     return {"width": win.winfo_screenwidth(), "height":win.winfo_screenheight()}
# #
# # def sendMessage(clientPhoneNumber):
# #     message = "Сообщение через for"
# #     pyautogui.moveTo(getScreenSize()["width"] * 0.694, getScreenSize()["height"] * 0.964)  # Moves the cursor the the message bar in Whatsapp
# #     pyautogui.click()
# #     pywhatkit.sendwhatmsg_instantly(phone_no=clientPhoneNumber, message=message)
# #     # pyautogui.press('enter')
# #     closeTab(5)
# #
# # def closeTab(waitTime):
# #     time.sleep(waitTime)
# #     _system = system().lower()
# #     if _system in ("windows", "linux"):
# #         pyautogui.hotkey("ctrl", "w")
# #     elif _system == "darwin":
# #         pyautogui.hotkey("command", "w")
# #     else:
# #         raise Warning(f"{_system} not supported!")
# #     pyautogui.press("enter")
# #
# # def sendTimeMessage(clientPhoneNumber, time):
# #     message = "Сообщение через for"
# #     hour = 0
# #     minutes = 0
# #     pywhatkit.sendwhatmsg(phone_no=clientPhoneNumber, message=message, time_hour=hour, time_min=minutes)
# #
# #
# # def main():
# #     sendMessage("+7 918 742-92-62")
# #     # image_to_ascii_art(img_path='hack_achiv.png')
# #
# #
# # if __name__ == '__main__':
# #   main()
#
#
# from selenium import webdriver
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from time import sleep
# #
# options = webdriver.ChromeOptions()
# options.add_argument('--allow-profiles-outside-user-dir')
# options.add_argument('--enable-profile-shortcut-manager')
# options.add_argument(r'user-data-dir=C:\Users\Lenovo\Desktop\Britva_bot\sel') # УКАЖИТЕ ПУТЬ ГДЕ ЛЕЖИТ ВАШ ФАЙЛ. Советую создать отдельную папку.
# options.add_argument('--profile-directory=Profile 1')
# options.add_argument('--profiling-flush=n')
# options.add_argument('--enable-aggressive-domstorage-flushing')
# # #
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# wait = WebDriverWait(driver, 30)
#
#
# number = "+79614951406"
# text = "Привет, это твой второй аккаунт!"
#
# url = f"https://web.whatsapp.com/send?phone={number}&text={text}"
# driver.get(url)
# wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#main > footer > div._2lSWV._3cjY2.copyable-area > div > span:nth-child(2) > div > div._1VZX7 > div._2xy_p._3XKXx > button > span")))
# driver.find_element(By.CSS_SELECTOR, "#main > footer > div._2lSWV._3cjY2.copyable-area > div > span:nth-child(2) > div > div._1VZX7 > div._2xy_p._3XKXx > button > span").click()
# sleep(5)