from fastapi import APIRouter, HTTPException, Depends
from config.databases import sql, cursor
from model.manager_models import Register  
from schema.manager_schema import list_serial  
from .auth_route import authenticate_user, Role  # Assuming you have an auth_route with authentication logic

manager_router = APIRouter()

@manager_router.post("/")
async def add_manager(info: Register, current_user: dict = Depends(authenticate_user)):
    """Add a new manager"""
    # Check if the user is admin or manager
    if current_user["role"] not in [Role.admin, Role.manager]:
        raise HTTPException(status_code=403, detail="Only admin or manager can add a manager")

    # If user is manager, make sure they are adding themselves as a manager
    if current_user["role"] == Role.manager and info.managerId != current_user["username"]:
        raise HTTPException(status_code=403, detail="Managers can only add themselves as managers")

    sql_query = "INSERT INTO manager VALUES (%s, %s);"
    try:
        cursor.execute(sql_query, (info.managerId, info.employeeId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Manager added successfully"}

@manager_router.get("/")
async def get_managers(current_user: dict = Depends(authenticate_user)):
    """Get all managers"""
    # Check if the user is admin or manager
    if current_user["role"] not in [Role.admin, Role.manager,Role.user]:
        raise HTTPException(status_code=403, detail="Only admin or manager or user can retrieve managers")

    sql_query = "SELECT * FROM manager;"
    try:
        cursor.execute(sql_query)
        managers = cursor.fetchall()
        result = list_serial(managers)  # Assuming you have a function to serialize manager data
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@manager_router.get("/{managerId}/employees/")
async def get_employee(managerId: str, current_user: dict = Depends(authenticate_user)):
    """Get employees corresponding to a manager"""
    # Check if the user is admin or manager
    if current_user["role"] not in [Role.admin, Role.manager,Role.user]:
        raise HTTPException(status_code=403, detail="Only admin or manager can view employees")

    # If user is manager, make sure they are retrieving employees for their own manager record
    if current_user["role"] == Role.manager and managerId != current_user["username"]:
        raise HTTPException(status_code=403, detail="Managers can only view employees for their own manager record")

    # Retrieve all employeeIds corresponding to the given manager ID
    sql_query = "SELECT employeeId FROM manager WHERE managerId = %s;"
    try:
        cursor.execute(sql_query, (managerId,))
        employees = cursor.fetchall()
        employee_ids = [emp[0] for emp in employees]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"managerId": managerId, "employees": employee_ids}




@manager_router.put("/{managerId}")
async def update_manager(managerId: str, old_employeeId: str, new_employeeId: str, current_user: dict = Depends(authenticate_user)):
    """Update manager"""
    # Check if the user is admin or manager
    if current_user["role"] not in [Role.admin, Role.manager]:
        raise HTTPException(status_code=403, detail="Only admin or manager can update managers")

    # If user is manager, make sure they are updating their own manager record
    if current_user["role"] == Role.manager and managerId != current_user["username"]:
        raise HTTPException(status_code=403, detail="Managers can only update their own manager records")

    sql_query = "UPDATE manager SET employeeId = %s WHERE managerId = %s AND employeeId = %s;"
    try:
        cursor.execute(sql_query, (new_employeeId, managerId, old_employeeId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Manager updated successfully"}


@manager_router.delete("/{managerId}")
async def delete_manager(managerId: str, employeeId: str, current_user: dict = Depends(authenticate_user)):
    """Delete manager"""
    # Check if the user is admin or manager
    if current_user["role"] not in [Role.admin, Role.manager]:
        raise HTTPException(status_code=403, detail="Only admin or manager can delete managers")

    # If user is manager, make sure they are deleting their own manager record
    if current_user["role"] == Role.manager and managerId != current_user["username"]:
        raise HTTPException(status_code=403, detail="Managers can only delete their own manager records")

    sql_query = "DELETE FROM manager WHERE managerId = %s AND employeeId = %s;"
    try:
        cursor.execute(sql_query, (managerId, employeeId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Manager deleted successfully"}
