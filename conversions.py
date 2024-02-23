import fnmatch
from urllib.parse import quote #quote нужна для преобразования текста в ссылку
from fnmatch import fnmatch
from datetime import datetime


def customerInfoProcessing(textMessage: str):
    message = textMessage.split()
    info = {"number":message[0], "date":message[1], "time":message[2]}
    return info

def checkPhoneNumber(phoneNumber : str):
    alphabet = "+0123456789" # пробел и "-" нужны для тех, кто пишет 8 999 99 99 или 8-999-99-99
    phoneNumber = phoneNormalized(phoneNumber)
    for symbol in phoneNumber:
        if not(symbol in alphabet):
            return "Проверьте корректность символов в номере!"
    if not(fnmatch(phoneNumber, "+7??????????") or fnmatch(phoneNumber, "8??????????")):
        return "Формат номера некорректен"
    return "OK"

def checkDate(date: str):
    if not(fnmatch(date, "??.??.??")):
        return "Проверьте дату на соответствие формату"

    alphabet = [str(i) for i in range(10)]
    if not(all([True if i in alphabet else False for i in date.replace(".", "")])):
        return "Дата должна состоять из цифр"
    dateNormal = dateNormalized(date)
    try:
        datetime(int(dateNormal["year"]), int(dateNormal["month"]), int(dateNormal["date"]))
    except:
        return "Введённая дата невозможна"
    return "OK"

def checkTime(time: str):
    timeNormal = timeNormalized(time)
    correctHours = [f"{i:02}" for i in range(0, 24)]
    correctMinutes = [f"{i:02}" for i in range(0, 60)]
    if not(fnmatch(time, "??:??")):
        return "Некорректная запись времени"
    if not((timeNormal["hour"] in correctHours) and (timeNormal["minutes"] in correctMinutes)):
        return "Введённое время невозможно"
    return "OK"

def phoneNormalized(phoneNumber : str):
    phoneNumber.replace("-","").replace("(", "").replace(")", "").replace(" ", "")
    return phoneNumber

def dateNormalized(date: str):
    date = date.split(".")
    dateDict = {"date":date[0], "month":date[1], "year":date[2]}
    return dateDict

def timeNormalized(time: str):
    time = time.split(":")
    timeDict = {"hour":time[0], "minutes":time[1]}
    return timeDict



def linkProcessing(phoneNumber, message):
    return "https://web.whatsapp.com/send?phone=" + phoneNumber + "&text=" + quote(message)
