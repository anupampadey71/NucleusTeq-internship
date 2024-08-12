import logging
import os
import hashlib
from enum import Enum
from logging.handlers import RotatingFileHandler
from fastapi import APIRouter, Form, HTTPException
from config.databases import get_db_connection

auth_router = APIRouter()

# Ensure the log directory exists
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)

# Configure logging for auth_route
auth_logger = logging.getLogger("auth")
auth_logger.setLevel(logging.INFO)

# Check if the logger already has handlers to avoid duplicate handlers
if not auth_logger.handlers:
    auth_file_handler = RotatingFileHandler(os.path.join(log_dir, 'auth.log'), maxBytes=1024 * 1024 * 10, backupCount=5)
    auth_file_handler.setLevel(logging.INFO)
    auth_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    auth_file_handler.setFormatter(auth_formatter)
    auth_logger.addHandler(auth_file_handler)

# Define roles
class Role(str, Enum):
    admin = "admin"
    manager = "manager"
    user = "user"

# Example dependency to authenticate and get user role
async def authenticate_user(username: str, password: str) -> dict:
    # Hash the password provided by the user using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        with get_db_connection() as (sql, cursor):
            # Query the database to retrieve the user with the provided username
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                # Retrieve the hashed password from the database
                stored_password_hash = user[2]  # Assuming the hashed password is in the third column

                # Verify the password by comparing the hashed password from the database
                # with the hashed password provided by the user
                if hashed_password == stored_password_hash:
                    auth_logger.info("User %s authenticated successfully", username)
                    return {"username": username, "role": user[3], "password": password}  # Assuming role is in the fourth column

        auth_logger.warning("Failed authentication attempt for user %s", username)
        return None
    except Exception as e:
        auth_logger.error("Error authenticating user %s: %s", username, str(e))
        return None

# Login endpoint to authenticate user
@auth_router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    user = await authenticate_user(username, password)
    if user:
        auth_logger.info("User %s logged in successfully", username)
        return {"token": "some_access_token", "username": user["username"], "role": user["role"], "password": user["password"]}  # You should implement proper token generation logic here
    else:
        auth_logger.warning("Invalid login attempt for user %s", username)
        raise HTTPException(status_code=401, detail="Invalid username or password")

# Change password endpoint
@auth_router.put("/change-password")
async def change_password(username: str = Form(...), old_password: str = Form(...), new_password: str = Form(...)):
    user = await authenticate_user(username, old_password)
    if user:
        # Hash the new password using SHA-256
        new_hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

        try:
            with get_db_connection() as (sql, cursor):
                # Update the password in the database
                cursor.execute("UPDATE users SET password_hash = %s WHERE username = %s", (new_hashed_password, username))
                sql.commit()
            auth_logger.info("Password updated successfully for user %s", username)
            return {"message": "Password updated successfully"}
        except Exception as e:
            auth_logger.error("Failed to update password for user %s: %s", username, str(e))
            raise HTTPException(status_code=500, detail="Failed to update password")
    else:
        auth_logger.warning("Failed password change attempt for user %s: Invalid old password", username)
        raise HTTPException(status_code=401, detail="Invalid username or old password")

# Ensure the logs are flushed properly
logging.shutdown()
