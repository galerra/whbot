from abstractBase import abstractBase
from databaseConfig import *
import psycopg2

class tableOffices(abstractBase):
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
                """CREATE TABLE offices(
                    office_id serial PRIMARY KEY,
                    company_name varchar(25) UNIQUE NOT NULL REFERENCES companies(company_name),
                    city varchar(25) NOT NULL,
                    street varchar(20) NOT NULL,
                    house SMALLINT NOT NULL,
                    building SMALLINT NOT NULL,
                    directorsSurname varchar(15) NOT NULL,
                    directorsName varchar(15) NOT NULL,
                    directorsPatronymic varchar(15) NOT NULL,
                    directorsTelegramId varchar(20) NOT NULL,
                    phone varchar(12) NOT NULL)"""
            )
    def insertToTable(self, data:tuple):
        with self.connection.cursor() as cursor:
            command = """INSERT INTO offices VALUES(DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(command, data)

    def __del__(self):
        self.connection.close()

db = tableOffices()
# db.createTable()
# db.insertToTable(('Britva', 'Новоалександровск', "Карла-Маркса", 180, 1, "Маслов", "Сергей", "Николаевич", "878095267", "+79064909665"))