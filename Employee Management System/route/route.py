from fastapi import APIRouter, HTTPException, Query
from config.databases import sql, cursor
from model.models import Register
from schema.schema import list_serial

router = APIRouter()

@router.post("/")
async def enter_employee_details(info: Register):
    # SQL injection vulnerability fixed by using parameterized queries
    sql_query = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s);"
    try:
        cursor.execute(sql_query, (info.employeeId, info.email, info.name, info.salary, info.role))
        sql.commit()
    except Exception as e:
        # HTTP 500 Internal Server Error if database operation fails
        raise HTTPException(status_code=500, detail=str(e))
    else:
        # Return success message
        return {"message": "Record added successfully"}

@router.get("/my_info")
async def my_info():
    sql_query = "SELECT * FROM employee;"
    try:
        cursor.execute(sql_query)
        values = cursor.fetchall()
        result = list_serial(values)
    except Exception as e:
        # HTTP 500 Internal Server Error if database operation fails
        raise HTTPException(status_code=500, detail=str(e))
    else:
        # Return data
        return result

@router.put("/{employeeId}")
async def update_name(employeeId: str, name: str):
    sql_query = "UPDATE employee SET name = %s WHERE employeeId = %s;"
    try:
        cursor.execute(sql_query, (name, employeeId))
        sql.commit()
    except Exception as e:
        # HTTP 500 Internal Server Error if database operation fails
        raise HTTPException(status_code=500, detail=str(e))
    else:
        # Return success message
        return {"message": "Record updated successfully"}

@router.delete("/")
async def delete_record(employeeId: str = Query(..., description="Employee ID")):
    sql_query = "DELETE FROM employee WHERE employeeId = %s;"
    try:
        cursor.execute(sql_query, (employeeId,))
        sql.commit()
    except Exception as e:
        # HTTP 500 Internal Server Error if database operation fails
        raise HTTPException(status_code=500, detail=str(e))
    else:
        # Return success message
        return {"message": "Record deleted successfully"}
