from dbFiles.tableStaff import Staff
from dbFiles.tableNotifications import Notifications
from fnmatch import fnmatch
from conversions import *


class Record():
    def __init__(self, info): #строка, которую отправляет админ с данными для записи
        if isinstance(info, tuple):
            self.id = str(info[0])
            info = [x for x in info[1::]] #обрезаем айди записи и превращаем тупл в массив
        else:
            self.id = "-1"
        data = info
        self.numberPhone = str(phoneNormalized(data[0]))
        self.date = str(dateNormalized(data[1]))
        self.time = str(data[2])
        self.adminId = str(data[3])
        if len(data) == 5:
            self.masterName = str(data[4])
        else:
            db = Staff()
            self.masterName = str(db.getName(self.adminId))



    def getData(self):
        return {"id": self.id, "numberPhone": self.numberPhone, "date": self.date, "time": self.time, "adminId": self.adminId, "masterName": self.masterName}

    def writeToDB(self):
        db = Notifications()
        db.insertToTable((number, date, time, adminId, masterName))

    def checkPhone(self):
        alphabet = "+0123456789"  # пробел и "-" нужны для тех, кто пишет 8 999 99 99 или 8-999-99-99
        phoneNumber = phoneNormalized(self.numberPhone)
        for symbol in phoneNumber:
            if not (symbol in alphabet):
                return "проверьте корректность символов в номере!"
        if not (fnmatch(phoneNumber, "+7??????????") or fnmatch(phoneNumber, "8??????????")):
            return "формат номера некорректен"
        return "OK"

    def checkDate(self):
        if not(fnmatch(self.date, "??.??.??") or fnmatch(self.date, "??.??.????")):
            return "проверьте дату на соответствие формату"
        alphabet = [str(i) for i in range(10)]
        if not(all([True if i in alphabet else False for i in self.date.replace(".", "")])):
            return "дата должна состоять из цифр"

        dateNormal = dateNormalized(self.date)
        dictDate = dateNormal.split(".")
        dictDate = {"date": dictDate[0], "month": dictDate[1], "year": dictDate[2]}
        try:
            datetime(int(dictDate["year"]), int(dictDate["month"]), int(dictDate["date"]))
        except:
            return "введённая дата невозможна"
        return "OK"

    def getIntDateTime(self):
        dateVisit = self.date.replace(".", " ").split()
        dateVisit = f"{dateVisit[2]}{dateVisit[1]}{dateVisit[0]}"
        timeVisit = self.time.replace(":", "")
        intDateTime = int(dateVisit + timeVisit)
        return intDateTime

    def recordCompare(self):
        dateCurrent = getCurrentDate()
        dateCurrent = dateCurrent.replace(".", " ").split()
        dateCurrent = f"{dateCurrent[2]}{dateCurrent[1]}{dateCurrent[0]}"
        timeCurrent = getCurrentTime()
        timeCurrent = timeCurrent.replace(":", "")
        recordCurrent = int(dateCurrent + timeCurrent)

        recordVisit = self.getIntDateTime()
        return recordVisit <= recordCurrent

    def checkTime(self):
        if not (fnmatch(self.time, "??:??")):
            return "некорректная запись времени"

        correctHours = [f"{i:02}" for i in range(0, 24)]
        correctMinutes = [f"{i:02}" for i in range(0, 60)]

        timeNormal = getTimeDict(self.time)
        if not((timeNormal["hour"] in correctHours) and (timeNormal["minutes"] in correctMinutes)):
            return "введённое время невозможно"
        if self.recordCompare():
            return "запись меньше текущих даты/времени"
        return "OK"


    def timeToRecord(self):
        currentTime = getTimeDict(getCurrentTime())
        recordTime = getTimeDict(self.time)
        print(currentTime, recordTime)
        time = (int(recordTime["hour"]) * 3600 + int(recordTime["minutes"]) * 60) - (int(currentTime["hour"]) * 3600 + int(currentTime["minutes"]) * 60)
        return time

