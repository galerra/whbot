from dbFiles.abstractBase import abstractBase
from dbFiles.databaseConfig import *
import psycopg2
import asyncio


class Staff(abstractBase):
    name = "staff"


    def createTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""CREATE TABLE {self.name}(
                    id serial PRIMARY KEY,
                    surname varchar(15) NOT NULL,
                    name varchar(15) NOT NULL,
                    patronymic varchar(15),
                    status varchar(10),
                    telegram_id varchar(20) NOT NULL,
                    phone varchar(12) NOT NULL
                    )"""
            )


    def insertToTable(self, data:tuple):
        with self.connection.cursor() as cursor:
            command = f"""INSERT INTO {self.name} VALUES(DEFAULT, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(command, data)


    def getStatus(self, telegramId):
        with self.connection.cursor() as cursor:
            command = f"""SELECT status FROM {self.name}
                         WHERE {self.name}.telegram_id = %s"""
            cursor.execute(command, (telegramId,))
            try:
                return cursor.fetchall()[0][0]
            except:
                return "customer"


    def getName(self, telegramId):
        with self.connection.cursor() as cursor:
            command = f"""SELECT name FROM {self.name}
                         WHERE staff.telegram_id = %s"""
            cursor.execute(command, (telegramId,))
            try:
                return cursor.fetchall()[0][0]
            except:
                return "NoName"

    def getPersonInfo(self, telegramId):
        with self.connection.cursor() as cursor:
            command = f"""SELECT * FROM {self.name}
                         WHERE {self.name}.telegram_id = %s"""
            cursor.execute(command, (telegramId,))
            try:
                data = cursor.fetchall()[0]
            except:
                return "NULL"
        columns = super().getColumnsNames()
        personInfo = {column:info for column, info in zip(columns, data)}
        return personInfo

    def getPhoneByStatus(self, status: str):
        with self.connection.cursor() as cursor:
            command = f"""SELECT phone FROM {self.name} WHERE status = %s"""
            cursor.execute(command, (status,))
            usersPhones = cursor.fetchall()[0]
        return usersPhones


    def deleteRecordByTelegramId(self, telegram_id: str):
        with self.connection.cursor() as cursor:
            command = f"""DELETE FROM {self.name} WHERE telegram_id = %s"""
            cursor.execute(command, (telegram_id,))



    def __del__(self):
        self.connection.close()

# db = Staff()
# print(db.selectData())
# print(db.getPhoneByStatus("admin"))
# print(db.getPersonInfo('815109033'))
# print(db.getColumnsNames())
