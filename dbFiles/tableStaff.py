from dbFiles.abstractBase import abstractBase
from dbFiles.databaseConfig import *
import psycopg2
import asyncio
class staff(abstractBase):
    def __init__(self):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        self.connection.autocommit = True

    def createTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE staff(
                    staff_id serial PRIMARY KEY,
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
            command = """INSERT INTO staff VALUES(DEFAULT, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(command, data)

    def getStatus(self, telegramId):
        with self.connection.cursor() as cursor:
            command = """SELECT status FROM staff
                         WHERE staff.telegram_id = %s"""
            cursor.execute(command, (telegramId,))
            return cursor.fetchall()[0][0]
    def getName(self, telegramId):
        with self.connection.cursor() as cursor:
            command = """SELECT name FROM staff
                         WHERE staff.telegram_id = %s"""
            cursor.execute(command, (telegramId,))
            return cursor.fetchall()[0][0]
    def selectData(self):
        with self.connection.cursor() as cursor:
            command = """SELECT * FROM staff"""
            cursor.execute(command)
            records = cursor.fetchall()
            return records
    def __del__(self):
        self.connection.close()

# db = staff()
# db.createTable()
# db.insertToTable(("Шуруха", "Артем", "Викторович", "creator", "815109033", "+79614951406"))

