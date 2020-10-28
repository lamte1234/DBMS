import mysql.connector

def user_connect():
    user_cnt = mysql.connector.connect(
        host='*',
        user='user',
        password='user',
        database='my_database',
        auth_plugin='mysql_native_password'
    )
    return user_cnt