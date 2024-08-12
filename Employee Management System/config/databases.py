import mysql.connector as sql_connector
from contextlib import contextmanager

# Database connection parameters
DB_PARAMS = {
    'host': 'mysql',
    'user': 'root',
    'passwd': 'BhaRas@123',
    'database': 'employee'
}

@contextmanager
def get_db_connection():
    """Context manager for managing the database connection and cursor."""
    connection = None
    cursor = None
    try:
        connection = sql_connector.connect(**DB_PARAMS)
        cursor = connection.cursor()
        yield connection, cursor
    except Exception as e:
        print(f"Error while connecting to the database: {e}")
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()