from dbFiles.databaseConfig import *
import psycopg2


class abstractBase(): #родительский класс для основных таблиц
    name = "abstract"
    def __init__(self, host = host, user = user, password = password, db_name = db_name):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        self.connection.autocommit = True
        self.name = self.__class__.name

    def isExist(self):
        with self.connection.cursor() as cursor:
            command = f"""select exists (select *
               from information_schema.tables
               where table_name = N'{self.name}'
                 and table_schema = 'public') as table_exists;"""
            cursor.execute(command, ())
            return cursor.fetchall()[0][0]

    def selectData(self):
        with self.connection.cursor() as cursor:
            command = f"""SELECT * FROM {self.name}"""
            cursor.execute(command, ())
            records = cursor.fetchall()
            return records


    def getColumnsNames(self):
        with self.connection.cursor() as cursor:
            command = f"""SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{self.name}'"""
            cursor.execute(command)
            records = cursor.fetchall()
        records = tuple([name[0] for name in records])
        return records

    def deleteData(self):
        with self.connection.cursor() as cursor:
            command = f"""TRUNCATE TABLE {self.name}"""
            cursor.execute(command)

    def deleteTable(self):
        with self.connection.cursor() as cursor:
            command = f"""DROP TABLE {self.name}"""
            cursor.execute(command)

    def deleteRecordById(self, idRecord : str):
        with self.connection.cursor() as cursor:
            command = f"""DELETE FROM {self.name} WHERE id = %s"""
            cursor.execute(command, (idRecord, ))

    def __del__(self):
        self.connection.close()


















