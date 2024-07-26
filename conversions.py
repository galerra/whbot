import fnmatch
from urllib.parse import quote #quote нужна для преобразования текста в ссылку
from fnmatch import fnmatch
from datetime import datetime
from user import User
from dbFiles.tableStaff import Staff

def getCurrentWeekday():
    current_weekday = datetime.today().weekday()
    return current_weekday

def getCurrentDay():
    current_day = datetime.now().day
    return current_day

def getCurrentMonth():
    current_month = datetime.now().month
    return current_month

def getCurrentYear():
    current_year = datetime.now().year
    return current_year


def getCurrentDate():
    day = str(datetime.now().day)
    month = str(datetime.now().month)
    year = str(datetime.now().year)
    date = dateNormalized(f"{day}.{month}.{year}")
    return date

def getCurrentTime():
    return str(datetime.now().time())[:5]


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

def getTimeDict(time: str):
    time = time.split(":")
    timeDict = {"hour":time[0], "minutes":time[1]}
    return timeDict

def getDateDict(date: str):
    date = date.split(".")
    dateDict = {"day": date[0], "month": date[1], "year": date[2]}
    return dateDict

def linkProcessing(phoneNumber, message):
    return "https://web.whatsapp.com/send?phone=" + phoneNumber + "&text=" + quote(message)


def getTextSortingRecords(records: list):
    db = Staff()
    workers = db.selectData()
    workers = [User(user[5]) for user in workers]

    text = ""
    for worker in workers:
        text += f"{worker.surname} {worker.name} {worker.patronymic}:\n"
        for record in records:
            if record.adminId == worker.telegramId:
                text += f"{record.numberPhone} {record.date} {record.time}\n"
        text += "\n"
    return text












