import os
import logging
from fastapi import APIRouter, HTTPException, Depends
from config.databases import sql, cursor
from model.manager_models import Register
from schema.manager_schema import list_serial
from .auth_route import authenticate_user, Role  # Assuming you have an auth_route with authentication logic

# Configure logging for manager_route
log_dir = "log"
manager_logger = logging.getLogger("manager")
manager_logger.setLevel(logging.INFO)

# Check if the logger already has handlers to avoid duplicate handlers
if not manager_logger.handlers:
    manager_file_handler = logging.FileHandler(os.path.join(log_dir, 'manager.log'))
    manager_file_handler.setLevel(logging.INFO)
    manager_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    manager_file_handler.setFormatter(manager_formatter)
    manager_logger.addHandler(manager_file_handler)

manager_router = APIRouter()

@manager_router.post("/")
async def add_manager(info: Register, current_user: dict = Depends(authenticate_user)):
    """Add a new manager"""
    try:
        # Check if the user is admin or manager
        if current_user["role"] not in [Role.admin, Role.manager]:
            manager_logger.warning("Unauthorized attempt to add manager by user %s", current_user["username"])
            raise HTTPException(status_code=403, detail="Only admin or manager can add a manager")

        # If user is manager, make sure they are adding themselves as a manager
        if current_user["role"] == Role.manager and info.managerId != current_user["username"]:
            manager_logger.warning("Manager %s attempted to add another manager %s", current_user["username"], info.managerId)
            raise HTTPException(status_code=403, detail="Managers can only add themselves as managers")

        # Check if the provided managerId exists in the employee table
        sql_query = "SELECT COUNT(*) FROM employee WHERE employeeId = %s;"
        cursor.execute(sql_query, (info.managerId,))
        result = cursor.fetchone()
        if result[0] == 0:
            raise HTTPException(status_code=404, detail="ManagerId does not exist in the employee table")

        sql_query = "INSERT INTO manager (managerId, employeeId) VALUES (%s, %s);"
        cursor.execute(sql_query, (info.managerId, info.employeeId))
        sql.commit()
        manager_logger.info("Manager %s and employee %s added successfully by user %s", info.managerId,info.employeeId, current_user["username"])
        return {"message": "Manager added successfully"}
    except Exception as e:
        manager_logger.error("Error adding manager %s: %s", info.managerId, str(e))
        raise HTTPException(status_code=500, detail=str(e))

@manager_router.get("/")
async def get_managers(current_user: dict = Depends(authenticate_user)):
    """Get all managers"""
    try:
        # Check if the user is admin or manager
        if current_user["role"] not in [Role.admin, Role.manager, Role.user]:
            manager_logger.warning("Unauthorized attempt to retrieve managers by user %s", current_user["username"])
            raise HTTPException(status_code=403, detail="Only admin, manager, or user can retrieve managers")

        sql_query = "SELECT * FROM manager;"
        cursor.execute(sql_query)
        managers = cursor.fetchall()
        result = list_serial(managers)  # Assuming you have a function to serialize manager data
        manager_logger.info("Retrieved all managers by user %s", current_user["username"])
        return result
    except Exception as e:
        manager_logger.error("Error retrieving managers: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@manager_router.get("/{managerId}/employees/")
async def get_employee(managerId: str, current_user: dict = Depends(authenticate_user)):
    """Get employees corresponding to a manager"""
    try:
        # Check if the user is admin or manager
        if current_user["role"] not in [Role.admin, Role.manager, Role.user]:
            manager_logger.warning("Unauthorized attempt to view employees by user %s", current_user["username"])
            raise HTTPException(status_code=403, detail="Only admin or manager can view employees")

        # If user is manager, make sure they are retrieving employees for their own manager record
        if current_user["role"] == Role.manager and managerId != current_user["username"]:
            manager_logger.warning("Manager %s attempted to view employees for another manager %s", current_user["username"], managerId)
            raise HTTPException(status_code=403, detail="Managers can only view employees for their own manager record")

        # Retrieve all employeeIds corresponding to the given manager ID
        sql_query = "SELECT employeeId FROM manager WHERE managerId = %s;"
        cursor.execute(sql_query, (managerId,))
        employees = cursor.fetchall()
        employee_ids = [emp[0] for emp in employees]
        manager_logger.info("Retrieved employees for manager %s by user %s", managerId, current_user["username"])
        return {"managerId": managerId, "employees": employee_ids}
    except Exception as e:
        manager_logger.error("Error retrieving employees for manager %s: %s", managerId, str(e))
        raise HTTPException(status_code=500, detail=str(e))

@manager_router.get("/user/manager/")
async def get_user_manager(current_user: dict = Depends(authenticate_user)):
    """Get the managerId corresponding to the logged-in user"""
    try:
        # Check if the user is a regular user
        if current_user["role"] != Role.user:
            manager_logger.warning("Unauthorized attempt to retrieve manager by user %s", current_user["username"])
            raise HTTPException(status_code=403, detail="Only regular users can retrieve their manager")

        # Retrieve the managerId for the logged-in user
        sql_query = "SELECT managerId FROM manager WHERE employeeId = %s;"
        cursor.execute(sql_query, (current_user["username"],))
        result = cursor.fetchone()
        if result is None:
            manager_logger.warning("Manager not found for user %s", current_user["username"])
            raise HTTPException(status_code=404, detail="Manager not found for the user")
        managerId = result[0]
        manager_logger.info("Retrieved managerId for user %s", current_user["username"])
        return {"managerId": managerId}
    except Exception as e:
        manager_logger.error("Error retrieving user manager: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@manager_router.put("/{managerId}")
async def update_manager(managerId: str, old_employeeId: str, new_employeeId: str, current_user: dict = Depends(authenticate_user)):
    """Update manager"""
    try:
        # Check if the user is admin or manager
        if current_user["role"] not in [Role.admin, Role.manager]:
            manager_logger.warning("Unauthorized attempt to update manager %s by user %s", managerId, current_user["username"])
            raise HTTPException(status_code=403, detail="Only admin or manager can update managers")

        # If user is manager, make sure they are updating their own manager record
        if current_user["role"] == Role.manager and managerId != current_user["username"]:
            manager_logger.warning("Manager %s attempted to update another manager %s", current_user["username"], managerId)
            raise HTTPException(status_code=403, detail="Managers can only update their own manager records")

        # Validate new_employeeId
        if not new_employeeId.startswith("EMP"):
            raise HTTPException(status_code=400, detail="New Employee ID must start with 'EMP'")

        sql_query = "UPDATE manager SET employeeId = %s WHERE managerId = %s AND employeeId = %s;"
        cursor.execute(sql_query, (new_employeeId, managerId, old_employeeId))
        sql.commit()
        manager_logger.info("Updated manager %s, old_employeeId %s to new_employeeId %s by user %s", managerId,old_employeeId,new_employeeId, current_user["username"])
        return {"message": "Manager updated successfully"}
    except Exception as e:
        manager_logger.error("Error updating manager %s: %s", managerId, str(e))
        raise HTTPException(status_code=500, detail=str(e))

@manager_router.delete("/{managerId}")
async def delete_manager(managerId: str, employeeId: str, current_user: dict = Depends(authenticate_user)):
    """Delete manager"""
    try:
        # Check if the user is admin or manager
        if current_user["role"] not in [Role.admin, Role.manager]:
            manager_logger.warning("Unauthorized attempt to delete manager %s by user %s", managerId, current_user["username"])
            raise HTTPException(status_code=403, detail="Only admin or manager can delete managers")

        # If user is manager, make sure they are deleting their own manager record
        if current_user["role"] == Role.manager and managerId != current_user["username"]:
            manager_logger.warning("Manager %s attempted to delete another manager %s", current_user["username"], managerId)
            raise HTTPException(status_code=403, detail="Managers can only delete their own manager records")

        sql_query = "DELETE FROM manager WHERE managerId = %s AND employeeId = %s;"
        cursor.execute(sql_query, (managerId, employeeId))
        sql.commit()
        manager_logger.info("Deleted manager %s and employee %s by user %s", managerId,employeeId, current_user["username"])
        return {"message": "Manager deleted successfully"}
    except Exception as e:
        manager_logger.error("Error deleting manager %s: %s", managerId, str(e))
        raise HTTPException(status_code=500, detail=str(e))
