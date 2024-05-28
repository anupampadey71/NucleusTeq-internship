import mysql.connector as sql_connector
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connect to MySQL database
try:
    sql = sql_connector.connect(host="localhost", user="root", passwd="BhaRas@123", database="employee")
    cursor = sql.cursor()
except Exception as e:
    print(e)
else:
    print("Successfully Connected !!!")

# # SQLAlchemy specific code
# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:BhaRas@123@localhost/employee"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# # Creating a session
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Creating base class for models
# Base = declarative_base()
