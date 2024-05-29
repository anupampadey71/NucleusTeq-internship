import mysql.connector as sql_connector
from fastapi import APIRouter, Form, HTTPException
import hashlib
from config.databases import sql, cursor
from enum import Enum  # Import database connection details

auth_router = APIRouter()

# Define roles
class Role(str, Enum):
    admin = "admin"
    manager = "manager"
    user = "user"

# Example dependency to authenticate and get user role
async def authenticate_user(username: str, password: str):
    # Hash the password provided by the user using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Query the database to retrieve the user with the provided username
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    
    if user:
        # Retrieve the hashed password from the database
        stored_password_hash = user[2]  # Assuming the hashed password is in the third column
        
        # Verify the password by comparing the hashed password from the database
        # with the hashed password provided by the user
        if hashed_password == stored_password_hash:
            return {"username": username, "role": user[3], "password": password}  # Assuming role is in the fourth column
    
    return None

# Login endpoint to authenticate user
@auth_router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    user = await authenticate_user(username, password)
    if user:
        return {"token": "some_access_token", "username": user["username"], "role": user["role"], "password": user["password"]}  # You should implement proper token generation logic here
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")