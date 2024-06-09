from dbFiles.abstractBase import abstractBase
from dbFiles.databaseConfig import *
import psycopg2
import asyncio
class history(abstractBase):
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
                """CREATE TABLE history(
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
            command = """INSERT INTO history VALUES(DEFAULT, %s, %s, %s, %s, %s)"""
            cursor.execute(command, data)

    def selectData(self):
        with self.connection.cursor() as cursor:
            command = """SELECT * FROM history"""
            cursor.execute(command)
            records = cursor.fetchall()
            return records
            # print(records)
    def deleteData(self):
        with self.connection.cursor() as cursor:
            command = """TRUNCATE TABLE history"""
            cursor.execute(command)
    def deleteTable(self):
        with self.connection.cursor() as cursor:
            command = """DROP TABLE history"""
            cursor.execute(command)
    def deleteRecord(self, idRecord:tuple):
        with self.connection.cursor() as cursor:
            command = """DELETE FROM history WHERE notifications_id = %s"""
            cursor.execute(command, idRecord)
    def __del__(self):
        self.connection.close()



# db = history()
# db.deleteDB()
# db.createTable()
# db.insertToTable(("26.03.2024", 226, "+79614951406"))
# db.selectData()