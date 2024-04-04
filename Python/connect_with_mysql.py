import mysql.connector  

# Creating the connection object     
conn_obj = mysql.connector.connect(host="localhost", user="root", passwd="12345")  

# creating the cursor object    
cur_obj = conn_obj.cursor()  

try:  
    # creating a new database using query   
    cur_obj.execute("create database Demo")  
    dbms = cur_obj.execute("show databases")  
except mysql.connector.Error as e:  
    conn_obj.rollback()   
    print("Error:", e)

for x in cur_obj:  
    print(x)  

conn_obj.close()
