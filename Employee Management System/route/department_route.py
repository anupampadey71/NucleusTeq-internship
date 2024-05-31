from fastapi import APIRouter, HTTPException, Query, Depends
from config.databases import sql, cursor
from model.department_models import Register
from schema.department_schema import list_serial
from .auth_route import authenticate_user, Role

department_router = APIRouter()

@department_router.post("/")
async def enter_department_details(info: Register, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin
    if current_user["role"] != Role.admin:
        raise HTTPException(status_code=403, detail="Only admin can add new departments")

    sql_query = "INSERT INTO department VALUES (%s, %s, %s);"
    try:
        cursor.execute(sql_query, (info.departmentId, info.name, info.managerId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Record added successfully"}

@department_router.get("/my_info")
async def my_info(current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin, user, or manager
    if current_user["role"] not in [Role.admin, Role.user, Role.manager]:
        raise HTTPException(status_code=403, detail="Only admin, user, or manager can access department info")

    sql_query = "SELECT * FROM department;"
    try:
        cursor.execute(sql_query)
        values = cursor.fetchall()
        result = list_serial(values)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return result

@department_router.put("/{departmentId}")
async def update_name(departmentId: str, name: str, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin
    if current_user["role"] != Role.admin:
        raise HTTPException(status_code=403, detail="Only admin can update department details")

    sql_query = "UPDATE department SET name = %s WHERE departmentId = %s;"
    try:
        cursor.execute(sql_query, (name, departmentId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Record updated successfully"}

@department_router.delete("/")
async def delete_record(departmentId: str = Query(..., description="Department ID"), current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin
    if current_user["role"] != Role.admin:
        raise HTTPException(status_code=403, detail="Only admin can delete department records")

    sql_query = "DELETE FROM department WHERE departmentId = %s;"
    try:
        cursor.execute(sql_query, (departmentId,))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Record deleted successfully"}