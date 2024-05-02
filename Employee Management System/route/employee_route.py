
from fastapi import APIRouter, HTTPException, Query
from config.databases import sql, cursor
from model.employee_models import Register
from schema.employee_schema import list_serial

employee_router = APIRouter()

@employee_router.post("/")
async def enter_employee_details(info: Register):
    sql_query = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s);"
    try:
        cursor.execute(sql_query, (info.employeeId, info.email, info.name, info.salary, info.role))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Record added successfully"}

@employee_router.get("/my_info")
async def my_info():
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
async def update_name(employeeId: str, name: str):
    sql_query = "UPDATE employee SET name = %s WHERE employeeId = %s;"
    try:
        cursor.execute(sql_query, (name, employeeId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Record updated successfully"}

@employee_router.delete("/")
async def delete_record(employeeId: str = Query(..., description="Employee ID")):
    sql_query = "DELETE FROM employee WHERE employeeId = %s;"
    try:
        cursor.execute(sql_query, (employeeId,))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Record deleted successfully"}
