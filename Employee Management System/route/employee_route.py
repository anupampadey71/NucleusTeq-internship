import logging
import os
import hashlib
from fastapi import APIRouter, HTTPException, Query, Depends
from config.databases import get_db_connection
from model.employee_models import Register, UpdateEmployeeDetails
from schema.employee_schema import list_serial
from .auth_route import authenticate_user, Role

employee_router = APIRouter()

# Ensure the log directory exists
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)

# Configure logging for employee_route
employee_logger = logging.getLogger("employee")
employee_logger.setLevel(logging.INFO)

# Check if the logger already has handlers to avoid duplicate handlers
if not employee_logger.handlers:
    employee_file_handler = logging.FileHandler(os.path.join(log_dir, 'employee.log'))
    employee_file_handler.setLevel(logging.INFO)
    employee_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    employee_file_handler.setFormatter(employee_formatter)
    employee_logger.addHandler(employee_file_handler)

@employee_router.post("/")
async def enter_employee_details(info: Register, current_user: dict = Depends(authenticate_user)):
    if current_user["role"] != Role.admin:
        employee_logger.warning("Unauthorized attempt to add employee by user %s", current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin can add new employees")

    employee_sql_query = "INSERT INTO employee (employeeId, email, name, salary, role) VALUES (%s, %s, %s, %s, %s);"
    user_sql_query = "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s);"

    # Determine role based on employeeId prefix
    if info.employeeId.startswith("EMP"):
        user_role = "user"
    elif info.employeeId.startswith("MGR"):
        user_role = "manager"
    elif info.employeeId.startswith("ADM"):
        user_role = "admin"
    else:
        employee_logger.warning("Invalid employeeId prefix: %s", info.employeeId)
        raise HTTPException(status_code=400, detail="Invalid employeeId prefix")

    # Hash the employeeId to use as the password
    hashed_password = hashlib.sha256(info.employeeId.encode()).hexdigest()

    try:
        with get_db_connection() as (sql, cursor):
            # Insert into employee table
            cursor.execute(employee_sql_query, (info.employeeId, info.email, info.name, info.salary, info.role))
            # Insert into users table
            cursor.execute(user_sql_query, (info.employeeId, hashed_password, user_role))
            sql.commit()
        employee_logger.info("Employee %s added successfully by user %s", info.employeeId, current_user["username"])
    except Exception as e:
        employee_logger.error("Error adding employee %s: %s", info.employeeId, str(e))
        raise HTTPException(status_code=500, detail=f"Error adding employee: {str(e)}")

    return {"message": "Record added successfully"}

@employee_router.get("/my_info")
async def my_info(current_user: dict = Depends(authenticate_user)):
    if current_user["role"] not in [Role.admin, Role.manager, Role.user]:
        employee_logger.warning("Unauthorized attempt to access employee info by user %s", current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin, manager, or employee can access employee info")

    sql_query = "SELECT * FROM employee;"
    try:
        with get_db_connection() as (sql, cursor):
            cursor.execute(sql_query)
            values = cursor.fetchall()
            result = list_serial(values)
        employee_logger.info("Employee info accessed by user %s", current_user["username"])
    except Exception as e:
        employee_logger.error("Error accessing employee info: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    
    return result

@employee_router.put("/{employeeId}")
async def update_employee_details(employeeId: str, info: UpdateEmployeeDetails, current_user: dict = Depends(authenticate_user)):
    if current_user["role"] != Role.admin:
        employee_logger.warning("Unauthorized attempt to update employee %s by user %s", employeeId, current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin can update employee details")

    sql_query = """
    UPDATE employee 
    SET email = %s, name = %s, salary = %s, role = %s
    WHERE employeeId = %s;
    """
    try:
        with get_db_connection() as (sql, cursor):
            cursor.execute(sql_query, (info.email, info.name, info.salary, info.role, employeeId))
            if cursor.rowcount == 0:
                employee_logger.warning("Employee %s not found for update by user %s", employeeId, current_user["username"])
                raise HTTPException(status_code=404, detail="Employee not found")
            sql.commit()
        employee_logger.info("Employee %s updated successfully by user %s", employeeId, current_user["username"])
    except Exception as e:
        employee_logger.error("Error updating employee %s: %s", employeeId, str(e))
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": "Record updated successfully"}

@employee_router.delete("/")
async def delete_record(employeeId: str = Query(..., description="Employee ID"), current_user: dict = Depends(authenticate_user)):
    if current_user["role"] != Role.admin:
        employee_logger.warning("Unauthorized attempt to delete employee %s by user %s", employeeId, current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin can delete employee records")

    delete_employee_sql_query = "DELETE FROM employee WHERE employeeId = %s;"
    delete_user_sql_query = "DELETE FROM users WHERE username = %s;"

    try:
        with get_db_connection() as (sql, cursor):
            # Delete from employee table
            cursor.execute(delete_employee_sql_query, (employeeId,))
            # Delete from users table
            cursor.execute(delete_user_sql_query, (employeeId,))
            if cursor.rowcount == 0:
                employee_logger.warning("Employee %s not found for deletion by user %s", employeeId, current_user["username"])
                raise HTTPException(status_code=404, detail="Employee not found")
            sql.commit()
        employee_logger.info("Employee %s deleted successfully by user %s", employeeId, current_user["username"])
    except Exception as e:
        employee_logger.error("Error deleting employee %s: %s", employeeId, str(e))
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": "Record deleted successfully"}
