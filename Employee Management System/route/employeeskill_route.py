from fastapi import APIRouter, HTTPException,Query
from config.databases import sql, cursor
from schema.employeeskill_schema import list_serial 
from model.employeeskill_models import Register

employeeskill_router = APIRouter()

@employeeskill_router.post("/")
async def create_employee_skill(info: Register):
    sql_query = "INSERT INTO employeeskill (employeeId, skillId) VALUES (%s, %s);"
    try:
        cursor.execute(sql_query, (info.employeeId, info.skillId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Employee skill association added successfully"}

@employeeskill_router.get("/{employeeId}")
async def get_employee_skills(employeeId: str):
    sql_query = "SELECT skillId FROM employeeskill WHERE employeeId = %s;"
    try:
        cursor.execute(sql_query, (employeeId,))
        values = cursor.fetchall()
        result = [value[0] for value in values]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"employeeId": employeeId, "skills": result}

@employeeskill_router.put("/")
async def update_employee_skill(employee_id: str = Query(..., description="Employee ID"),
                               current_skill_id: str = Query(..., description="Current Skill ID"),
                               new_skill_id: str = Query(..., description="New Skill ID")):
    sql_query = "UPDATE employeeskill SET skillId = %s WHERE employeeId = %s AND skillId = %s;"
    try:
        cursor.execute(sql_query, (new_skill_id, employee_id, current_skill_id))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": f"Employee skill association updated successfully for employee {employee_id}"}



@employeeskill_router.delete("/{employeeId}/{skillId}")
async def delete_employee_skill(employeeId: str, skillId: str):
    sql_query = "DELETE FROM employeeskill WHERE employeeId = %s AND skillId = %s;"
    try:
        cursor.execute(sql_query, (employeeId, skillId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Employee skill association deleted successfully"}
