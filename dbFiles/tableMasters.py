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
                """CREATE TABLE masters(
                    master_id serial PRIMARY KEY,
                    office_id integer REFERENCES offices(office_id),
                    surname varchar(15) NOT NULL,
                    name varchar(15) NOT NULL,
                    patronymic varchar(15),
                    telegram_id varchar(20) NOT NULL,
                    phone varchar(12) NOT NULL)"""
            )
    def insertToTable(self, data:tuple):
        with self.connection.cursor() as cursor:
            command = """INSERT INTO masters VALUES(DEFAULT, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(command, data)

    def __del__(self):
        self.connection.close()

# db = tableOffices()
# db.createTable()
# db.insertToTable(("1", "Шуруха", "Артем", "Викторович", "815109033", "+79614951406"))