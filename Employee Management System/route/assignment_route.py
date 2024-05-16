from fastapi import APIRouter, HTTPException, Query, Depends
from config.databases import sql, cursor
from model.assignment_models import Register
from schema.assignment_schema import list_serial
from .auth_route import authenticate_user, Role

assignment_router = APIRouter()

@assignment_router.post("/")
async def create_assignment(assignment: Register):
    """Create a new assignment."""
    sql_query = "INSERT INTO assignment (assignmentId, requestId, employeeId, projectId, status) VALUES (%s, %s, %s, %s, %s);"
    try:
        cursor.execute(sql_query, (assignment.assignmentId, assignment.requestId, assignment.employeeId, assignment.projectId, assignment.status))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Assignment added successfully"}

@assignment_router.get("/all_assignments")
async def get_all_assignments():
    """Retrieve all assignments."""
    sql_query = "SELECT * FROM assignment;"
    try:
        cursor.execute(sql_query)
        values = cursor.fetchall()
        result = list_serial(values)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return result

@assignment_router.put("/{assignmentId}")
async def update_assignment(assignmentId: str, status: str):
    """Update the status of an assignment."""
    sql_query = "UPDATE assignment SET status = %s WHERE assignmentId = %s;"
    try:
        cursor.execute(sql_query, (status, assignmentId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Assignment status updated successfully"}

@assignment_router.delete("/{assignmentId}")
async def delete_assignment(assignmentId: str):
    """Delete an assignment."""
    sql_query = "DELETE FROM assignment WHERE assignmentId = %s;"
    try:
        cursor.execute(sql_query, (assignmentId,))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Assignment deleted successfully"}