import logging
import os
from fastapi import APIRouter, HTTPException, Depends
from config.databases import sql, cursor
from model.request_models import Register
from schema.request_schema import list_serial
from .auth_route import authenticate_user, Role

request_router = APIRouter()

# Ensure the log directory exists
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)

# Configure logging for request_router
request_logger = logging.getLogger("request")
request_file_handler = logging.handlers.RotatingFileHandler(os.path.join(log_dir, 'request.log'), maxBytes=1024 * 1024 * 10, backupCount=5)
request_file_handler.setLevel(logging.INFO)
request_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
request_file_handler.setFormatter(request_formatter)
request_logger.addHandler(request_file_handler)

def get_manager_id(project_id: str):
    """Get managerId associated with the project_id."""
    sql_query = "SELECT managerId FROM project WHERE projectId = %s;"
    cursor.execute(sql_query, (project_id,))
    manager = cursor.fetchone()
    return manager[0] if manager else None

@request_router.post("/")
async def create_request(request: Register, current_user: dict = Depends(authenticate_user)):
    """Create a new request."""
    # Only managers can create requests for their projects
    if current_user["role"] != Role.manager or get_manager_id(request.projectId) != current_user["username"]:
        request_logger.warning("Unauthorized attempt to create request for project %s by user %s", request.projectId, current_user["username"])
        raise HTTPException(status_code=403, detail="Only managers can create requests for their projects")

    sql_query = "INSERT INTO request VALUES (%s, %s, %s, %s);"
    try:
        cursor.execute(sql_query, (request.requestId, request.projectId, request.skillId, request.status))
        sql.commit()
        request_logger.info("Request %s created successfully for project %s by user %s", request.requestId, request.projectId, current_user["username"])
    except Exception as e:
        request_logger.error("Error creating request %s for project %s: %s", request.requestId, request.projectId, str(e))
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": "Request added successfully"}

@request_router.get("/all_requests")
async def get_all_requests(current_user: dict = Depends(authenticate_user)):
    """Retrieve all requests."""
    if current_user["role"] == Role.manager:
        # Managers can access requests associated with their projects or their own requests
        manager_id = current_user["username"]
        sql_query = "SELECT projectId FROM project WHERE managerId = %s;"
        cursor.execute(sql_query, (manager_id,))
        project_ids = cursor.fetchall()
        if project_ids:
            project_ids = [project[0] for project in project_ids]
            project_ids_str = ", ".join(["%s" for _ in project_ids])
            sql_query = f"SELECT * FROM request WHERE projectId IN ({project_ids_str});"
            cursor.execute(sql_query, project_ids)
        else:
            # If no projects found for the manager, return empty list
            request_logger.info("No projects found for manager %s", current_user["username"])
            return {"requests": []}
    elif current_user["role"] == Role.admin:
        # Admins can access all requests
        sql_query = "SELECT * FROM request;"
        cursor.execute(sql_query)
    else:
        # Regular users and other roles don't have access
        request_logger.warning("Unauthorized attempt to access all requests by user %s", current_user["username"])
        raise HTTPException(status_code=403, detail="You don't have permission to access this resource")

    # Fetch all requests
    requests = cursor.fetchall()
    request_logger.info("All requests retrieved successfully by user %s", current_user["username"])
    return {"requests": requests}

@request_router.put("/{requestId}")
async def update_request(requestId: str, status: str, current_user: dict = Depends(authenticate_user)):
    """Update the status of a request."""
    # Retrieve projectId from the database using the requestId
    sql_query = "SELECT projectId FROM request WHERE requestId = %s;"
    cursor.execute(sql_query, (requestId,))
    result = cursor.fetchone()
    if not result:
        request_logger.warning("Request %s not found for update by user %s", requestId, current_user["username"])
        raise HTTPException(status_code=404, detail="Request not found")
    projectId = result[0]

    # Only managers can update requests for their projects
    if current_user["role"] != Role.manager or get_manager_id(projectId) != current_user["username"]:
        request_logger.warning("Unauthorized attempt to update request %s for project %s by user %s", requestId, projectId, current_user["username"])
        raise HTTPException(status_code=403, detail="Only managers can update requests for their projects")

    # Update request status in the database
    sql_query = "UPDATE request SET status = %s WHERE requestId = %s;"
    try:
        cursor.execute(sql_query, (status, requestId))
        sql.commit()
        request_logger.info("Request %s updated successfully for project %s by user %s", requestId, projectId, current_user["username"])
    except Exception as e:
        request_logger.error("Error updating request %s for project %s: %s", requestId, projectId, str(e))
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": "Request status updated successfully"}

@request_router.delete("/{requestId}")
async def delete_request(requestId: str, current_user: dict = Depends(authenticate_user)):
    """Delete a request."""
    # Retrieve projectId from the database using the requestId
    sql_query = "SELECT projectId FROM request WHERE requestId = %s;"
    cursor.execute(sql_query, (requestId,))
    result = cursor.fetchone()
    if not result:
        request_logger.warning("Request %s not found for deletion by user %s", requestId, current_user["username"])
        raise HTTPException(status_code=404, detail="Request not found")
    projectId = result[0]

    # Only managers can delete requests for their projects
    if current_user["role"] != Role.manager or get_manager_id(projectId) != current_user["username"]:
        request_logger.warning("Unauthorized attempt to delete request %s for project %s by user %s", requestId, projectId, current_user["username"])
        raise HTTPException(status_code=403, detail="Only managers can delete requests for their projects")

    # Delete the request from the database
    sql_query = "DELETE FROM request WHERE requestId = %s;"
    try:
        cursor.execute(sql_query, (requestId,))
        sql.commit()
        request_logger.info("Request %s deleted successfully for project %s by user %s", requestId, projectId, current_user["username"])
    except Exception as e:
        request_logger.error("Error deleting request %s for project %s: %s", requestId, projectId, str(e))
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": "Request deleted successfully"}
