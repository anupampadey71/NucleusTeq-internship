import logging
import os
from fastapi import APIRouter, HTTPException, Depends
from config.databases import sql, cursor
from model.skillset_models import Register
from schema.skillset_schema import list_serial
from .auth_route import authenticate_user, Role

skillset_router = APIRouter()

# Ensure the log directory exists
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)

# Configure logging for skillset_route
skillset_logger = logging.getLogger("skillset")
skillset_file_handler = logging.handlers.RotatingFileHandler(os.path.join(log_dir, 'skillset.log'), maxBytes=1024 * 1024 * 10, backupCount=5)
skillset_file_handler.setLevel(logging.INFO)
skillset_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
skillset_file_handler.setFormatter(skillset_formatter)
skillset_logger.addHandler(skillset_file_handler)

@skillset_router.post("/")
async def create_skillset(info: Register, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin
    if current_user["role"] != Role.admin:
        skillset_logger.warning("Unauthorized attempt to create skill by user %s", current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin can create skills")

    sql_query = "INSERT INTO skillset (skillId, skillName) VALUES (%s, %s);"
    try:
        cursor.execute(sql_query, (info.skillId, info.skillName))
        sql.commit()
        skillset_logger.info("Skill %s added successfully by user %s", info.skillId, current_user["username"])
        return {"message": "Skill added successfully"}
    except Exception as e:
        skillset_logger.error("Error adding skill %s: %s", info.skillId, str(e))
        raise HTTPException(status_code=500, detail=str(e))

@skillset_router.get("/all_skills")
async def get_all_skills(current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin, manager, or user
    if current_user["role"] not in [Role.admin, Role.manager, Role.user]:
        skillset_logger.warning("Unauthorized attempt to retrieve skills by user %s", current_user["username"])
        raise HTTPException(status_code=403, detail="Only employees can retrieve all skills")

    sql_query = "SELECT * FROM skillset;"
    try:
        cursor.execute(sql_query)
        values = cursor.fetchall()
        skillset_logger.info("Skills retrieved by user %s", current_user["username"])
        return list_serial(values)
    except Exception as e:
        skillset_logger.error("Error retrieving skills: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@skillset_router.put("/{skillId}")
async def update_skill_name(skillId: str, name: str, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin
    if current_user["role"] != Role.admin:
        skillset_logger.warning("Unauthorized attempt to update skill %s by user %s", skillId, current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin can update skill names")

    sql_query = "UPDATE skillset SET skillName = %s WHERE skillId = %s;"
    try:
        cursor.execute(sql_query, (name, skillId))
        sql.commit()
        skillset_logger.info("Skill %s updated successfully by user %s", skillId, current_user["username"])
        return {"message": "Skill name updated successfully"}
    except Exception as e:
        skillset_logger.error("Error updating skill %s: %s", skillId, str(e))
        raise HTTPException(status_code=500, detail=str(e))

@skillset_router.delete("/{skillId}")
async def delete_skill(skillId: str, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin
    if current_user["role"] != Role.admin:
        skillset_logger.warning("Unauthorized attempt to delete skill %s by user %s", skillId, current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin can delete skills")

    sql_query = "DELETE FROM skillset WHERE skillId = %s;"
    try:
        cursor.execute(sql_query, (skillId,))
        sql.commit()
        skillset_logger.info("Skill %s deleted successfully by user %s", skillId, current_user["username"])
        return {"message": "Skill deleted successfully"}
    except Exception as e:
        skillset_logger.error("Error deleting skill %s: %s", skillId, str(e))
        raise HTTPException(status_code=500, detail=str(e))
