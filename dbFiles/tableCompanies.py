from abstractBase import abstractBase
from databaseConfig import *
import psycopg2
from tabulate import tabulate
class tableCompanies(abstractBase):
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
                """CREATE TABLE companies(
                    company_id serial PRIMARY KEY,
                    company_name varchar(25) UNIQUE NOT NULL,
                    data_payment date NOT NULL,
                    owner_surname varchar(15) NOT NULL,
                    owner_name varchar(15) NOT NULL,
                    owner_patronymic varchar(15) NOT NULL,
                    owner_telegram_id varchar(20) NOT NULL,
                    owner_phone varchar(12) NOT NULL)"""
            )

    def insertToTable(self, data:tuple):
        with self.connection.cursor() as cursor:
            command = """INSERT INTO companies VALUES(DEFAULT, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(command, data)

    def selectFromTable(self):
        with self.connection.cursor() as cursor:
            command = """SELECT * FROM  companies"""
            cursor.execute(command)
            records = cursor.fetchall()
            command = """SELECT Column_Name
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_NAME = 'companies'
                        ORDER BY Column_Name ASC"""
            cursor.execute(command)
            columnsNames = cursor.fetchall()
        columnsNames = [name[0] for name in columnsNames]
        print(tabulate(records, headers= (columnsNames)))
    def getOwnersTelegramId(self):
        with self.connection.cursor() as cursor:
            command = """SELECT owner_telegram_id
                            FROM companies"""
            cursor.execute(command)
            return cursor.fetchall()

    def __del__(self):
        self.connection.close()

db = tableCompanies()
# db.createTable()
db.insertToTable(('Britvaa', '2024-05-03', 'Маслов', 'Сергей', 'Николаевич', '878095267', '+79064909665'))
# db.selectFromTable()
