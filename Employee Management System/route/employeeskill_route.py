from fastapi import APIRouter, HTTPException, Query, Depends
from config.databases import sql, cursor
from .auth_route import authenticate_user, Role
from schema.employeeskill_schema import list_serial 
from model.employeeskill_models import Register

employeeskill_router = APIRouter()

@employeeskill_router.post("/")
async def create_employee_skill(info: Register, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin or user
    if current_user["role"] not in [Role.admin, Role.user]:
        raise HTTPException(status_code=403, detail="Only admin or user can add employee skills")

    # If user is user, make sure they can only add skills for themselves
    if current_user["role"] == Role.user and info.employeeId != current_user["username"]:
        raise HTTPException(status_code=403, detail="Users can only add skills for themselves")

    sql_query = "INSERT INTO employeeskill (employeeId, skillId) VALUES (%s, %s);"
    try:
        cursor.execute(sql_query, (info.employeeId, info.skillId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Employee skill association added successfully"}

@employeeskill_router.get("/{employeeId}")
async def get_employee_skills(employeeId: str, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin, manager, or user
    if current_user["role"] not in [Role.admin, Role.manager, Role.user]:
        raise HTTPException(status_code=403, detail="Only admin, manager, or user can view employee skills")

    # If user is user, make sure they can only view skills for themselves or their employees
    if current_user["role"] == Role.user:
        if employeeId != current_user["username"]:
            raise HTTPException(status_code=403, detail="Users can only view skills for themselves or their employees")
        # If employeeId and username are the same, allow access to all skills for that employeeId
        else:
            sql_query = "SELECT skillId FROM employeeskill WHERE employeeId = %s;"
            try:
                cursor.execute(sql_query, (employeeId,))
                values = cursor.fetchall()
                result = [value[0] for value in values]
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            else:
                return {"employeeId": employeeId, "skills": result}

    
    elif current_user["role"] in [Role.admin, Role.manager]:
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
                               new_skill_id: str = Query(..., description="New Skill ID"),
                               current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin or user
    if current_user["role"] not in [Role.admin, Role.user]:
        raise HTTPException(status_code=403, detail="Only admin or user can update employee skills")

    # If user is user, make sure they can only update skills for themselves
    if current_user["role"] == Role.user and employee_id != current_user["username"]:
        raise HTTPException(status_code=403, detail="Users can only update their own skills")

    sql_query = "UPDATE employeeskill SET skillId = %s WHERE employeeId = %s AND skillId = %s;"
    try:
        cursor.execute(sql_query, (new_skill_id, employee_id, current_skill_id))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": f"Employee skill association updated successfully for employee {employee_id}"}

@employeeskill_router.delete("/{employeeId}/{skillId}")
async def delete_employee_skill(employeeId: str, skillId: str, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin or user
    if current_user["role"] not in [Role.admin, Role.user]:
        raise HTTPException(status_code=403, detail="Only admin or user can delete employee skills")

    # If user is user, make sure they can only delete skills for themselves
    if current_user["role"] == Role.user and employeeId != current_user["username"]:
        raise HTTPException(status_code=403, detail="Users can only delete their own skills")

    sql_query = "DELETE FROM employeeskill WHERE employeeId = %s AND skillId = %s;"
    try:
        cursor.execute(sql_query, (employeeId, skillId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Employee skill association deleted successfully"}