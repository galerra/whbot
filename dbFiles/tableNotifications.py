from dbFiles.abstractBase import abstractBase
from dbFiles.databaseConfig import *
import psycopg2
import asyncio
class notifications(abstractBase):
    def __init__(self):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        self.connection.autocommit = True

    def createTable(self):  #я храню только минуты от начала дня
        with self.connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE notifications(
                    notification_id serial PRIMARY KEY,
                    visit_date varchar(10) NOT NULL,
                    visit_time varchar(5) NOT NULL,
                    client_phone varchar(12) NOT NULL,
                    admin_id varchar(20), 
                    master_name varchar(20)
                    )"""
            )
    def insertToTable(self, data:tuple):
        with self.connection.cursor() as cursor:
            command = """INSERT INTO notifications VALUES(DEFAULT, %s, %s, %s, %s, %s)"""
            cursor.execute(command, data)

    def selectData(self):
        with self.connection.cursor() as cursor:
            command = """SELECT * FROM  notifications"""
            cursor.execute(command)
            records = cursor.fetchall()
            return records
            # print(records)
    def deleteData(self):
        with self.connection.cursor() as cursor:
            command = """TRUNCATE TABLE notifications"""
            cursor.execute(command)
    def deleteTable(self):
        with self.connection.cursor() as cursor:
            command = """DROP TABLE notifications"""
            cursor.execute(command)
    def __del__(self):
        self.connection.close()



# db = notifications()
# db.deleteDB()
# db.createTable()
# db.insertToTable(("26.03.2024", 226, "+79614951406"))
# db.selectData()