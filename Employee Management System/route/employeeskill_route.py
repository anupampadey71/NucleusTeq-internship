import logging
import os
from fastapi import APIRouter, HTTPException, Query, Depends
from config.databases import get_db_connection
from .auth_route import authenticate_user, Role
from schema.employeeskill_schema import list_serial 
from model.employeeskill_models import Register

employeeskill_router = APIRouter()

# Ensure the log directory exists
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)

# Configure logging for employeeskill_router
employeeskill_logger = logging.getLogger("employeeskill")
employeeskill_logger.setLevel(logging.INFO)

# Check if the logger already has handlers to avoid duplicate handlers
if not employeeskill_logger.handlers:
    employeeskill_file_handler = logging.FileHandler(os.path.join(log_dir, 'employeeskill.log'))
    employeeskill_file_handler.setLevel(logging.INFO)
    employeeskill_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    employeeskill_file_handler.setFormatter(employeeskill_formatter)
    employeeskill_logger.addHandler(employeeskill_file_handler)

@employeeskill_router.post("/")
async def create_employee_skill(info: Register, current_user: dict = Depends(authenticate_user)):
    if current_user["role"] not in [Role.admin, Role.user]:
        employeeskill_logger.warning("Unauthorized attempt to add employee skill by user %s", current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin or user can add employee skills")

    if current_user["role"] == Role.user and info.employeeId != current_user["username"]:
        employeeskill_logger.warning("User %s attempted to add skill for another employee", current_user["username"])
        raise HTTPException(status_code=403, detail="Users can only add skills for themselves")

    sql_query = "INSERT INTO employeeskill (employeeId, skillId) VALUES (%s, %s);"
    try:
        with get_db_connection() as (sql, cursor):
            cursor.execute(sql_query, (info.employeeId, info.skillId))
            sql.commit()
        employeeskill_logger.info("Employee %s and skill %s association added successfully by user %s", info.employeeId, info.skillId, current_user["username"])
    except Exception as e:
        employeeskill_logger.error("Error adding employee skill: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Employee skill association added successfully"}

@employeeskill_router.get("/{employeeId}")
async def get_employee_skills(employeeId: str, current_user: dict = Depends(authenticate_user)):
    if current_user["role"] not in [Role.admin, Role.manager, Role.user]:
        employeeskill_logger.warning("Unauthorized attempt to view employee skills by user %s", current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin, manager, or user can view employee skills")

    if current_user["role"] == Role.user and employeeId != current_user["username"]:
        employeeskill_logger.warning("User %s attempted to view skills for another employee", current_user["username"])
        raise HTTPException(status_code=403, detail="Users can only view skills for themselves")

    sql_query = "SELECT skillId FROM employeeskill WHERE employeeId = %s;"
    try:
        with get_db_connection() as (sql, cursor):
            cursor.execute(sql_query, (employeeId,))
            values = cursor.fetchall()
            result = [value[0] for value in values]
        employeeskill_logger.info("Employee skills retrieved successfully by user %s", current_user["username"])
    except Exception as e:
        employeeskill_logger.error("Error retrieving employee skills: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

    return {"employeeId": employeeId, "skills": result}

@employeeskill_router.put("/")
async def update_employee_skill(employee_id: str = Query(..., description="Employee ID"),
                                current_skill_id: str = Query(..., description="Current Skill ID"),
                                new_skill_id: str = Query(..., description="New Skill ID"),
                                current_user: dict = Depends(authenticate_user)):
    if current_user["role"] not in [Role.admin, Role.user]:
        employeeskill_logger.warning("Unauthorized attempt to update employee skill by user %s", current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin or user can update employee skills")

    if current_user["role"] == Role.user and employee_id != current_user["username"]:
        employeeskill_logger.warning("User %s attempted to update skill for another employee", current_user["username"])
        raise HTTPException(status_code=403, detail="Users can only update their own skills")

    sql_query = "UPDATE employeeskill SET skillId = %s WHERE employeeId = %s AND skillId = %s;"
    try:
        with get_db_connection() as (sql, cursor):
            cursor.execute(sql_query, (new_skill_id, employee_id, current_skill_id))
            sql.commit()
        employeeskill_logger.info("Employee skill association updated successfully for employee %s, old_skill %s, new_skill %s by user %s", employee_id, current_skill_id, new_skill_id, current_user["username"])
    except Exception as e:
        employeeskill_logger.error("Error updating employee skill: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": f"Employee skill association updated successfully for employee {employee_id}"}

@employeeskill_router.delete("/{employeeId}/{skillId}")
async def delete_employee_skill(employeeId: str, skillId: str, current_user: dict = Depends(authenticate_user)):
    if current_user["role"] not in [Role.admin, Role.user]:
        employeeskill_logger.warning("Unauthorized attempt to delete employee skill by user %s", current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin or user can delete employee skills")

    if current_user["role"] == Role.user and employeeId != current_user["username"]:
        employeeskill_logger.warning("User %s attempted to delete skill for another employee", current_user["username"])
        raise HTTPException(status_code=403, detail="Users can only delete their own skills")

    sql_query = "DELETE FROM employeeskill WHERE employeeId = %s AND skillId = %s;"
    try:
        with get_db_connection() as (sql, cursor):
            cursor.execute(sql_query, (employeeId, skillId))
            sql.commit()
        employeeskill_logger.info("Employee skill association deleted successfully for employee %s and skillId %s by user %s", employeeId, skillId, current_user["username"])
    except Exception as e:
        employeeskill_logger.error("Error deleting employee skill: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Employee skill association deleted successfully"}
