import mysql.connector as sql_connector

# Connect to MySQL database
try:
    sql = sql_connector.connect(host="mysql", user="root", passwd="BhaRas@123", database="employee")
    cursor = sql.cursor()
except Exception as e:
    print(e)
else:
    print("Successfully Connected !!!")

def get_db_connection():
    return sql, cursor
