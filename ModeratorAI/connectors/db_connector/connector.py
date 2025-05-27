import psycopg2
from psycopg2 import sql
import os
import sys

sys.path.append(os.getcwd())

from source.config import psql_host, psql_dbname, psql_password, psql_port, psql_user

def validate_chat(user_id, chat_id):
    try:
        connection = psycopg2.connect(
            host=psql_host,
            port=psql_port,
            dbname=psql_dbname,
            user=psql_user,
            password=psql_password
        )
        cursor = connection.cursor()

        check_query = '''
            SELECT EXISTS (
                SELECT 1 FROM users WHERE user_id = %s and chat_id = %s
            );
        '''

        cursor.execute(check_query, (user_id, chat_id))
        exists = cursor.fetchone()[0]
        connection.close()
        
        return exists
    except Exception as ex:
        print(f"Error {ex}")

def add_user(user_id, chat_id, violnce, terrorism, racism, politics):
    try:
        connection = psycopg2.connect(
            host=psql_host,
            port=psql_port,
            dbname=psql_dbname,
            user=psql_user,
            password=psql_password
        )
        cursor = connection.cursor()

        # SQL query for inserting data
        query = '''
            INSERT INTO users (user_id, chat_id, violence, terrorism, racism, politics)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''

        print((user_id, chat_id, violnce, terrorism, racism, politics))

        cursor.execute(query, tuple(map(str ,(user_id, chat_id, violnce, terrorism, racism, politics))))
        connection.commit()
        connection.close()
    except Exception as ex:
        print(f"Error {ex}")
