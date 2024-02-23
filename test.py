host = "127.0.0.1"
user = "postgres"
password = "12345"
db_name = "postgres"

import psycopg2
try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database= db_name
    )

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )
        print(f"Server version: {cursor.fetchone()}")
except:
    print("No")






















