import os
import logging
import logging.handlers
from fastapi import APIRouter, HTTPException, Depends
from config.databases import sql, cursor
from model.project_models import Register, UpdateProject
from schema.project_schema import list_serial
from .auth_route import authenticate_user, Role

# Create a log directory if it doesn't exist
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)

# Configure logging for project_route
project_logger = logging.getLogger("project")
project_logger.setLevel(logging.INFO)  # Set log level to INFO

project_file_handler = logging.handlers.RotatingFileHandler(os.path.join(log_dir, 'project.log'), maxBytes=1024 * 1024 * 10, backupCount=5)
project_file_handler.setLevel(logging.INFO)
project_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
project_file_handler.setFormatter(project_formatter)
project_logger.addHandler(project_file_handler)

project_router = APIRouter()

@project_router.post("/")
async def create_project(project: Register, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin or manager
    if current_user["role"] not in [Role.admin, Role.manager]:
        project_logger.warning("Unauthorized attempt to create project by user %s", current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin or manager can create projects")

    # If the user is a manager, ensure the managerId matches their username
    if current_user["role"] == Role.manager and project.managerId != current_user["username"]:
        project_logger.warning("Manager %s tried to create a project with managerId %s", current_user["username"], project.managerId)
        raise HTTPException(status_code=403, detail="Managers can only create projects for themselves")

    # Check if the managerId exists in the employee table
    sql_query_check_manager = "SELECT employeeId FROM employee WHERE employeeId = %s;"
    cursor.execute(sql_query_check_manager, (project.managerId,))
    manager = cursor.fetchone()
    if not manager:
        project_logger.warning("Attempt to create project with non-existing managerId %s by user %s", project.managerId, current_user["username"])
        raise HTTPException(status_code=400, detail="managerId does not exist")

    sql_query = "INSERT INTO project (projectId, name, description, managerId) VALUES (%s, %s, %s, %s);"
    try:
        cursor.execute(sql_query, (project.projectId, project.name, project.description, project.managerId))
        sql.commit()
        project_logger.info("Project %s created successfully by user %s", project.projectId, current_user["username"])
        return {"message": "Project added successfully"}
    except Exception as e:
        project_logger.error("Error creating project %s: %s", project.projectId, str(e))
        raise HTTPException(status_code=500, detail=str(e))

@project_router.get("/all_projects")
async def get_all_projects(current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin, manager, or user
    if current_user["role"] not in [Role.admin, Role.manager, Role.user]:
        project_logger.warning("Unauthorized attempt to retrieve all projects by user %s", current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin, manager, or user can retrieve all projects")

    sql_query = "SELECT * FROM project;"
    try:
        cursor.execute(sql_query)
        values = cursor.fetchall()
        project_logger.info("All projects retrieved successfully by user %s", current_user["username"])
        return list_serial(values)
    except Exception as e:
        project_logger.error("Error retrieving all projects: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@project_router.put("/{projectId}")
async def update_project(projectId: str, project: UpdateProject, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin or manager
    if current_user["role"] not in [Role.admin, Role.manager]:
        project_logger.warning("Unauthorized attempt to update project %s by user %s", projectId, current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin or manager can update projects")

    # If the user is a manager, ensure the managerId matches their username
    if current_user["role"] == Role.manager and project.managerId != current_user["username"]:
        project_logger.warning("Manager %s tried to update a project with managerId %s", current_user["username"], project.managerId)
        raise HTTPException(status_code=403, detail="Managers can only update projects for themselves")

    # Check if the managerId exists in the employee table
    sql_query_check_manager = "SELECT employeeId FROM employee WHERE employeeId = %s;"
    cursor.execute(sql_query_check_manager, (project.managerId,))
    manager = cursor.fetchone()
    if not manager:
        project_logger.warning("Attempt to update project with non-existing managerId %s by user %s", project.managerId, current_user["username"])
        raise HTTPException(status_code=400, detail="managerId does not exist")

    # Check if the projectId exists
    sql_query_check = "SELECT managerId FROM project WHERE projectId = %s;"
    try:
        cursor.execute(sql_query_check, (projectId,))
        result = cursor.fetchone()
        if not result:
            project_logger.warning("Project %s not found for update by user %s", projectId, current_user["username"])
            raise HTTPException(status_code=404, detail="Project not found")
    except Exception as e:
        project_logger.error("Error checking project %s for update: %s", projectId, str(e))
        raise HTTPException(status_code=500, detail=str(e))

    sql_query = "UPDATE project SET name = %s, description = %s, managerId = %s WHERE projectId = %s;"
    try:
        cursor.execute(sql_query, (project.name, project.description, project.managerId, projectId))
        sql.commit()
        project_logger.info("Project %s updated successfully by user %s", projectId, current_user["username"])
        return {"message": "Project updated successfully"}
    except Exception as e:
        project_logger.error("Error updating project %s: %s", projectId, str(e))
        raise HTTPException(status_code=500, detail=str(e))

@project_router.delete("/{projectId}")
async def delete_project(projectId: str, current_user: dict = Depends(authenticate_user)):
    # Check if the user is admin or manager
    if current_user["role"] not in [Role.admin, Role.manager]:
        project_logger.warning("Unauthorized attempt to delete project %s by user %s", projectId, current_user["username"])
        raise HTTPException(status_code=403, detail="Only admin or manager can delete projects")

    # Check if the projectId exists
    sql_query_check = "SELECT managerId FROM project WHERE projectId = %s;"
    try:
        cursor.execute(sql_query_check, (projectId,))
        result = cursor.fetchone()
        if not result:
            project_logger.warning("Project %s not found for deletion by user %s", projectId, current_user["username"])
            raise HTTPException(status_code=404, detail="Project not found")
    except Exception as e:
        project_logger.error("Error checking project %s for deletion: %s", projectId, str(e))
        raise HTTPException(status_code=500, detail=str(e))

    # Check if the current user is the manager assigned to the project
    if current_user["role"] == Role.manager and result[0] != current_user["username"]:
        project_logger.warning("Manager %s tried to delete project %s which is not assigned to them", current_user["username"], projectId)
        raise HTTPException(status_code=403, detail="You can only delete projects assigned to you")

    # Perform deletion
    sql_query = "DELETE FROM project WHERE projectId = %s;"
    try:
        cursor.execute(sql_query, (projectId,))
        sql.commit()
        project_logger.info("Project %s deleted successfully by user %s", projectId, current_user["username"])
        return {"message": "Project deleted successfully"}
    except Exception as e:
        project_logger.error("Error deleting project %s: %s", projectId, str(e))
        raise HTTPException(status_code=500, detail=str(e))
