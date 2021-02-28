import mysql.connector
import os


def rfam_db_con():
    return mysql.connector.connect(
        host=os.getenv("RFAM_DB_HOST"),
        port=os.getenv("RFAM_DB_PORT"),
        user=os.getenv("RFAM_DB_USER"),
        password=os.getenv("RFAM_DB_PASS"),
        database=os.getenv("RFAM_DB_DATABASE"))

def query_alltime(sql):
    connection = rfam_db_con()
    cursor = connection.cursor(dictionary=True, buffered=True)

    cursor.execute(sql)
    res = cursor.fetchall()
    connection.close()
    return res


def query_timeframe(sql,date_start,date_end):
    connection = rfam_db_con()
    cursor = connection.cursor(dictionary=True, buffered=True)
    date_start = date_start.strftime('%Y-%m-%d')
    date_end = date_end.strftime('%Y-%m-%d')
    cursor.execute(sql, (date_start, date_end))
    res = cursor.fetchall()
    connection.close()
    return res