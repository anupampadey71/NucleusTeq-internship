from fastapi import APIRouter, HTTPException, Depends
from config.databases import sql, cursor
from model.skillset_models import Register
from schema.skillset_schema import list_serial
from .auth_route import authenticate_user, Role

skillset_router = APIRouter()


@skillset_router.post("/")
async def create_skillset(info: Register, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin
    if current_user["role"] != Role.admin:
        raise HTTPException(status_code=403, detail="Only admin can create skills")

    sql_query = "INSERT INTO skillset VALUES (%s, %s);"
    try:
        cursor.execute(sql_query, (info.skillId, info.skillName))
        sql.commit()
        return {"message": "Skill added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@skillset_router.get("/all_skills")
async def get_all_skills(current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin
    if current_user["role"] not in [Role.admin, Role.manager, Role.user]:
        raise HTTPException(status_code=403, detail="Only employee can retrieve all skills")

    sql_query = "SELECT * FROM skillset;"
    try:
        cursor.execute(sql_query)
        values = cursor.fetchall()
        return list_serial(values)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@skillset_router.put("/{skillId}")
async def update_skill_name(skillId: str, name: str, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin
    if current_user["role"] != Role.admin:
        raise HTTPException(status_code=403, detail="Only admin can update skill names")

    sql_query = "UPDATE skillset SET skillName = %s WHERE skillId = %s;"
    try:
        cursor.execute(sql_query, (name, skillId))
        sql.commit()
        return {"message": "Skill name updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@skillset_router.delete("/{skillId}")
async def delete_skill(skillId: str, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin
    if current_user["role"] != Role.admin:
        raise HTTPException(status_code=403, detail="Only admin can delete skills")

    sql_query = "DELETE FROM skillset WHERE skillId = %s;"
    try:
        cursor.execute(sql_query, (skillId,))
        sql.commit()
        return {"message": "Skill deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
