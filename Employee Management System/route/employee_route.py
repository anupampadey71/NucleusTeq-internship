from fastapi import APIRouter, HTTPException, Query, Depends
from config.databases import sql, cursor
from model.employee_models import Register, UpdateEmployeeDetails
from schema.employee_schema import list_serial
from .auth_route import authenticate_user, Role

employee_router = APIRouter()

@employee_router.post("/")
async def enter_employee_details(info: Register, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin
    if current_user["role"] != Role.admin:
        raise HTTPException(status_code=403, detail="Only admin can add new employees")

    sql_query = "INSERT INTO employee (employeeId, email, name, salary, role) VALUES (%s, %s, %s, %s, %s);"
    try:
        cursor.execute(sql_query, (info.employeeId, info.email, info.name, info.salary, info.role))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Record added successfully"}

@employee_router.get("/my_info")
async def my_info(current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin, manager, or user
    if current_user["role"] not in [Role.admin, Role.manager, Role.user]:
        raise HTTPException(status_code=403, detail="Only admin, manager, or employee can access employee info")

    sql_query = "SELECT * FROM employee;"
    try:
        cursor.execute(sql_query)
        values = cursor.fetchall()
        result = list_serial(values)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return result

@employee_router.put("/{employeeId}")
async def update_employee_details(employeeId: str, info: UpdateEmployeeDetails, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin
    if current_user["role"] != Role.admin:
        raise HTTPException(status_code=403, detail="Only admin can update employee details")

    sql_query = """
    UPDATE employee 
    SET email = %s, name = %s, salary = %s, role = %s, is_assigned = %s
    WHERE employeeId = %s;
    """
    try:
        cursor.execute(sql_query, (info.email, info.name, info.salary, info.role, info.is_assigned, employeeId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Record updated successfully"}

@employee_router.delete("/")
async def delete_record(employeeId: str = Query(..., description="Employee ID"), current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin
    if current_user["role"] != Role.admin:
        raise HTTPException(status_code=403, detail="Only admin can delete employee records")

    sql_query = "DELETE FROM employee WHERE employeeId = %s;"
    try:
        cursor.execute(sql_query, (employeeId,))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Record deleted successfully"}
