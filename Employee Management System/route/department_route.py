import logging
import os
from fastapi import APIRouter, HTTPException, Query, Depends
from config.databases import sql, cursor
from model.department_models import Register
from schema.department_schema import list_serial
from .auth_route import authenticate_user, Role

department_router = APIRouter()

# Ensure the log directory exists
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)

# Configure logging for department_route
department_logger = logging.getLogger("department")
department_logger.setLevel(logging.INFO)

# Check if the logger already has handlers to avoid duplicate handlers
if not department_logger.handlers:
    department_file_handler = logging.FileHandler(os.path.join(log_dir, 'department.log'))
    department_file_handler.setLevel(logging.INFO)
    department_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    department_file_handler.setFormatter(department_formatter)
    department_logger.addHandler(department_file_handler)


@department_router.post("/")
async def enter_department_details(info: Register, current_user: dict = Depends(authenticate_user)):
    if current_user["role"] != Role.admin:
        department_logger.warning("Unauthorized attempt to add department by user %s", current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin can add new departments")

    sql_query = "INSERT INTO department VALUES (%s, %s, %s);"
    try:
        cursor.execute(sql_query, (info.departmentId, info.name, info.managerId))
        sql.commit()
        department_logger.info("Department %s added successfully by user %s", info.departmentId, current_user["username"])
    except Exception as e:
        department_logger.error("Error adding department %s: %s", info.departmentId, str(e))
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Record added successfully"}


@department_router.get("/my_info")
async def my_info(current_user: dict = Depends(authenticate_user)):
    if current_user["role"] not in [Role.admin, Role.user, Role.manager]:
        department_logger.warning("Unauthorized attempt to access department info by user %s", current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin, user, or manager can access department info")

    sql_query = "SELECT * FROM department;"
    try:
        cursor.execute(sql_query)
        values = cursor.fetchall()
        result = list_serial(values)
        department_logger.info("Department info accessed by user %s", current_user["username"])
    except Exception as e:
        department_logger.error("Error accessing department info: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    return result


@department_router.put("/{departmentId}")
async def update_name(departmentId: str, name: str, current_user: dict = Depends(authenticate_user)):
    if current_user["role"] != Role.admin:
        department_logger.warning("Unauthorized attempt to update department %s by user %s", departmentId, current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin can update department details")

    sql_query = "UPDATE department SET name = %s WHERE departmentId = %s;"
    try:
        cursor.execute(sql_query, (name, departmentId))
        if cursor.rowcount == 0:
            department_logger.warning("Department %s not found for update by user %s", departmentId, current_user["username"])
            raise HTTPException(status_code=404, detail="Department not found")
        sql.commit()
        department_logger.info("Department %s updated to %s by user %s", departmentId, name, current_user["username"])
    except Exception as e:
        department_logger.error("Error updating department %s: %s", departmentId, str(e))
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Record updated successfully"}


@department_router.delete("/")
async def delete_record(departmentId: str = Query(..., description="Department ID"), current_user: dict = Depends(authenticate_user)):
    if current_user["role"] != Role.admin:
        department_logger.warning("Unauthorized attempt to delete department %s by user %s", departmentId, current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin can delete department records")

    sql_query = "DELETE FROM department WHERE departmentId = %s;"
    try:
        cursor.execute(sql_query, (departmentId,))
        if cursor.rowcount == 0:
            department_logger.warning("Department %s not found for deletion by user %s", departmentId, current_user["username"])
            raise HTTPException(status_code=404, detail="Department not found")
        sql.commit()
        department_logger.info("Department %s deleted by user %s", departmentId, current_user["username"])
    except Exception as e:
        department_logger.error("Error deleting department %s: %s", departmentId, str(e))
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Record deleted successfully"}
