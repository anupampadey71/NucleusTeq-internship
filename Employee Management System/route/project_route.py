from fastapi import APIRouter, HTTPException, Depends
from config.databases import sql, cursor
from model.project_models import Register, UpdateProject
from schema.project_schema import list_serial
from .auth_route import authenticate_user, Role

project_router = APIRouter()

@project_router.post("/")
async def create_project(project: Register, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin or manager
    if current_user["role"] not in [Role.admin, Role.manager]:
        raise HTTPException(status_code=403, detail="Only admin or manager can create projects")

    # Check if the managerId matches the current user's username
    if current_user["role"] == Role.manager and project.managerId != current_user["username"]:
        raise HTTPException(status_code=403, detail="You are only allowed to create projects for yourself")

    sql_query = "INSERT INTO project (projectId, name, description, managerId) VALUES (%s, %s, %s, %s);"
    try:
        cursor.execute(sql_query, (project.projectId, project.name, project.description, project.managerId))
        sql.commit()
        return {"message": "Project added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@project_router.get("/all_projects")
async def get_all_projects(current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin or manager
    if current_user["role"] not in [Role.admin, Role.manager,Role.user]:
        raise HTTPException(status_code=403, detail="Only admin or manager or user can retrieve all projects")

    sql_query = "SELECT * FROM project;"
    try:
        cursor.execute(sql_query)
        values = cursor.fetchall()
        return list_serial(values)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@project_router.put("/{projectId}")
async def update_project(projectId: str, project: UpdateProject, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin
    if current_user["role"] not in [Role.admin, Role.manager]:
        raise HTTPException(status_code=403, detail="Only admin or manager can update projects")


    # Check if the managerId matches the current user's username
    if current_user["role"] == Role.manager and project.managerId != current_user["username"]:
        raise HTTPException(status_code=403, detail="You are only allowed to update projects for yourself")

    # Check if the projectId exists and if the managerId matches the current user's username
    sql_query_check = "SELECT managerId FROM project WHERE projectId = %s;"
    try:
        cursor.execute(sql_query_check, (projectId,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Project not found")
        elif current_user["role"] == Role.manager and result[0] != current_user["username"]:
            raise HTTPException(status_code=403, detail="You are only allowed to update your own projects")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    sql_query = "UPDATE project SET name = %s, description = %s, managerId = %s WHERE projectId = %s;"
    try:
        cursor.execute(sql_query, (project.name, project.description, project.managerId, projectId))
        sql.commit()
        return {"message": "Project updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@project_router.delete("/{projectId}")
async def delete_project(projectId: str, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin or manager
    if current_user["role"] not in [Role.admin, Role.manager]:
        raise HTTPException(status_code=403, detail="Only admin or manager can delete projects")

    # Check if the projectId exists
    sql_query_check = "SELECT managerId FROM project WHERE projectId = %s;"
    try:
        cursor.execute(sql_query_check, (projectId,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Project not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Check if the current user is the manager assigned to the project
    if current_user["role"] == Role.manager and result[0] != current_user["username"]:
        raise HTTPException(status_code=403, detail="You can only delete projects assigned to you")

    # Perform deletion
    sql_query = "DELETE FROM project WHERE projectId = %s;"
    try:
        cursor.execute(sql_query, (projectId,))
        sql.commit()
        return {"message": "Project deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
