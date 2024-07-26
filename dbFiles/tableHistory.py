from dbFiles.abstractBase import abstractBase
from dbFiles.databaseConfig import *
import psycopg2
import asyncio


class History(abstractBase):
    name = "history"

    def createTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""CREATE TABLE {self.name}(
                    id serial PRIMARY KEY,
                    client_phone varchar(12) NOT NULL,
                    visit_date varchar(10) NOT NULL,
                    visit_time varchar(5) NOT NULL,
                    admin_id varchar(20), 
                    master_name varchar(20)
                    )"""
            )
    def insertToTable(self, data:tuple):
        with self.connection.cursor() as cursor:
            command = f"""INSERT INTO {self.name} VALUES(DEFAULT, %s, %s, %s, %s, %s)"""
            cursor.execute(command, data)

    def __del__(self):
        self.connection.close()



# db = History()
# db.deleteTable()
# db.createTable()
# db.insertToTable(("26.03.2024", 226, "+79614951406"))
# print(db.selectData())