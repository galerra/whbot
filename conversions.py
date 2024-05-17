import fnmatch
from urllib.parse import quote #quote нужна для преобразования текста в ссылку
from fnmatch import fnmatch
from datetime import datetime
from dbFiles.tableStaff import staff

# def convertMinutes(time):
#     time = time.split(":")
#     time = int(time[0]) * 60 + int(time[1])
#     return time


def getCurrentDate():
    day = str(datetime.now().day)
    month = str(datetime.now().month)
    year = str(datetime.now().year)
    date = dateNormalized(f"{day}.{month}.{year}")
    return date

def getCurrentTime():
    return str(datetime.now().time())[:5]

def customerInfoProcessing(Message):
    message = Message.text.split()
    info = {"number":message[0], "date":message[1], "time":message[2], "adminId":Message.from_user.id}
    if len(message) == 4:
        info["masterName"] = message[3]
    else:
        masterId = str(Message.from_user.id)
        db = staff()
        masterName = db.getName(masterId)
        info["masterName"] = masterName
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
    if not(fnmatch(date, "??.??.??") or fnmatch(date, "??.??.????")):
        return "Проверьте дату на соответствие формату"
    if not(dateCompare(date, getCurrentDate())):
        return "Введённая дата меньше текущей"
    alphabet = [str(i) for i in range(10)]
    if not(all([True if i in alphabet else False for i in date.replace(".", "")])):
        return "Дата должна состоять из цифр"
    dateNormal = dateNormalized(date).split(".")
    dateNormal = {"date":dateNormal[0], "month":dateNormal[1], "year":dateNormal[2]}
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
    day, month, year = date[0], date[1], date[2]
    day = "0" + day if len(day) == 1 else day
    month = "0" + month if len(month) == 1 else month
    year = "20" + year if len(year) == 2 else year
    return f"{day}.{month}.{year}"

def timeNormalized(time: str):
    time = time.split(":")
    timeDict = {"hour":time[0], "minutes":time[1]}
    return timeDict


def timeCompare(timeVisit: str, timeCurrent: str):
    timeVisit = int(timeVisit.replace(":", ""))
    timeCurrent = int(timeCurrent.replace(":", ""))
    return timeCurrent >= timeVisit

def dateCompare(dateVisit: str, dateCurrent:str):
    dateVisit = int(dateVisit.replace(":", ""))
    dateCurrent = int(dateCurrent.replace(":", ""))
    return dateCurrent >= dateVisit


def linkProcessing(phoneNumber, message):
    return "https://web.whatsapp.com/send?phone=" + phoneNumber + "&text=" + quote(message)