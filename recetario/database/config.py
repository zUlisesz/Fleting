from passkey import PASS
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password=PASS,
        database='coocking'
    )

conn = get_connection()
