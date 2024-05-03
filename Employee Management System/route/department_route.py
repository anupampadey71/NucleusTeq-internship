# department_route.py

from fastapi import APIRouter, HTTPException, Query
from config.databases import sql, cursor
from model.department_models import Register  # Changed import
from schema.department_schema import list_serial

department_router = APIRouter()

@department_router.post("/")
async def enter_department_details(info: Register):  # Changed function name
    sql_query = "INSERT INTO department VALUES (%s, %s, %s);"
    try:
        cursor.execute(sql_query, (info.departmentId, info.name, info.managerId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Record added successfully"}

@department_router.get("/my_info")
async def my_info():
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
async def update_name(departmentId: str, name: str):
    sql_query = "UPDATE department SET name = %s WHERE departmentId = %s;"
    try:
        cursor.execute(sql_query, (name, departmentId))  # Changed parameter name
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Record updated successfully"}

@department_router.delete("/")
async def delete_record(departmentId: str = Query(..., description="Department ID")):
    sql_query = "DELETE FROM department WHERE departmentId = %s;"
    try:
        cursor.execute(sql_query, (departmentId,))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Record deleted successfully"}



# @department_router.get("/departments")
# async def get_departments():
#     sql_query = "SELECT * FROM department;"
#     try:
#         cursor.execute(sql_query)
#         departments = cursor.fetchall()
#         return {"departments": departments}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
