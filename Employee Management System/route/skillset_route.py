from fastapi import APIRouter, HTTPException, Query
from config.databases import sql, cursor
from model.skillset_models import Register  
from schema.skillset_schema import list_serial 

skillset_router = APIRouter()

@skillset_router.post("/")
async def create_skillset(info: Register):
    sql_query = "INSERT INTO skillset VALUES (%s, %s);"
    try:
        cursor.execute(sql_query, (info.skillId, info.skillName))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Skill added successfully"}

@skillset_router.get("/all_skills")
async def get_all_skills():
    sql_query = "SELECT * FROM skillset;"
    try:
        cursor.execute(sql_query)
        values = cursor.fetchall()
        result = list_serial(values)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return result

@skillset_router.put("/{skillId}")
async def update_skill_name(skillId: str, name: str):
    sql_query = "UPDATE skillset SET skillName = %s WHERE skillId = %s;"
    try:
        cursor.execute(sql_query, (name, skillId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Skill name updated successfully"}

@skillset_router.delete("/{skillId}")
async def delete_skill(skillId: str ):   #= Query(..., description="Skill ID")
    sql_query = "DELETE FROM skillset WHERE skillId = %s;"
    try:
        cursor.execute(sql_query, (skillId,))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Skill deleted successfully"}
