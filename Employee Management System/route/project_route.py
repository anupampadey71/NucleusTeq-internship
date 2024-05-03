from fastapi import APIRouter, HTTPException
from config.databases import sql, cursor
from model.project_models import Register
from schema.project_schema import list_serial

project_router = APIRouter()

@project_router.post("/")
async def create_project(project: Register):
    """Create a new project."""
    sql_query = "INSERT INTO project VALUES (%s, %s, %s);"
    try:
        cursor.execute(sql_query, (project.projectId, project.name, project.description))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Project added successfully"}

@project_router.get("/all_projects")
async def get_all_projects():
    """Retrieve all projects."""
    sql_query = "SELECT * FROM project;"
    try:
        cursor.execute(sql_query)
        values = cursor.fetchall()
        result = list_serial(values)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return result

@project_router.put("/{projectId}")
async def update_project(projectId: str, name: str, description: str):
    """Update the name and description of a project."""
    sql_query = "UPDATE project SET name = %s, description = %s WHERE projectId = %s;"
    try:
        cursor.execute(sql_query, (name, description, projectId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Project updated successfully"}

@project_router.delete("/{projectId}")
async def delete_project(projectId: str):
    """Delete a project."""
    sql_query = "DELETE FROM project WHERE projectId = %s;"
    try:
        cursor.execute(sql_query, (projectId,))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Project deleted successfully"}
