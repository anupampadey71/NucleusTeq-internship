import logging
import os
from fastapi import APIRouter, HTTPException, Depends
from config.databases import sql, cursor
from model.assignment_models import Register, create_assignment
from schema.assignment_schema import list_serial
from .auth_route import authenticate_user, Role

# Create a log folder if it doesn't exist
log_folder = "log"
os.makedirs(log_folder, exist_ok=True)

# Configure logging for assignment_route
assignment_logger = logging.getLogger("assignment")
assignment_logger.setLevel(logging.INFO)
assignment_file_handler = logging.handlers.RotatingFileHandler(
    os.path.join(log_folder, 'assignment.log'), maxBytes=1024 * 1024 * 10, backupCount=5)
assignment_file_handler.setLevel(logging.INFO)
assignment_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
assignment_file_handler.setFormatter(assignment_formatter)
assignment_logger.addHandler(assignment_file_handler)

assignment_router = APIRouter()

@assignment_router.post("/")
async def create_assignment(assignment: create_assignment, current_user: dict = Depends(authenticate_user)):
    """Create a new assignment."""
    try:
        if current_user["role"] != Role.admin:
            assignment_logger.warning("Unauthorized attempt to create assignment by user %s", current_user["username"])
            raise HTTPException(status_code=403, detail="Only admin can create assignments")

        # Check if request status is 'Open'
        cursor.execute("SELECT status FROM request WHERE requestId = %s", (assignment.requestId,))
        request_status = cursor.fetchone()
        if not request_status or request_status[0] != 'Open':
            assignment_logger.warning("Request %s is not open", assignment.requestId)
            raise HTTPException(status_code=400, detail="Request is not open")

        # Check if the employee is available
        cursor.execute("SELECT is_assigned FROM employee WHERE employeeId = %s", (assignment.employeeId,))
        employee_status = cursor.fetchone()
        if not employee_status or employee_status[0] != 0:
            assignment_logger.warning("Employee %s is not available", assignment.employeeId)
            raise HTTPException(status_code=400, detail="Employee is not available")

        # Check if the employee has the required skill
        cursor.execute("SELECT skillId FROM employeeskill WHERE employeeId = %s", (assignment.employeeId,))
        employee_skills = cursor.fetchall()
        cursor.execute("SELECT skillId FROM request WHERE requestId = %s", (assignment.requestId,))
        required_skill = cursor.fetchone()
        
        # Extract the required skill ID
        required_skill_id = required_skill[0] if required_skill else None
        if required_skill_id not in [skill[0] for skill in employee_skills]:
            assignment_logger.warning("Employee %s does not have the required skill %s", assignment.employeeId, required_skill_id)
            raise HTTPException(status_code=400, detail="Employee does not have the required skill")

        # Insert the assignment
        cursor.execute("INSERT INTO assignment (assignmentId, requestId, employeeId, projectId, assigned) VALUES (%s, %s, %s, %s, %s)", 
                       (assignment.assignmentId, assignment.requestId, assignment.employeeId, assignment.projectId, False))
        sql.commit()
        assignment_logger.info("Assignment %s created successfully by user %s", assignment.assignmentId, current_user["username"])
        return {"message": "Assignment added successfully"}
    except Exception as e:
        assignment_logger.error("Error creating assignment %s: %s", assignment.assignmentId, str(e))
        raise HTTPException(status_code=500, detail=str(e))

@assignment_router.get("/all_assignments")
async def get_all_assignments(current_user: dict = Depends(authenticate_user)):
    """Retrieve all assignments."""
    try:
        if current_user["role"] == Role.admin:
            sql_query = "SELECT * FROM assignment ORDER BY assignmentId ASC;"
            cursor.execute(sql_query)
        elif current_user["role"] == Role.user:
            sql_query = "SELECT * FROM assignment WHERE employeeId = %s ORDER BY assignmentId ASC;"
            cursor.execute(sql_query, (current_user["username"],))
        elif current_user["role"] == Role.manager:
            sql_query = """
                SELECT a.*
                FROM assignment a
                JOIN project p ON a.projectId = p.projectId
                WHERE p.managerId = %s
                ORDER BY a.assignmentId ASC;
            """
            cursor.execute(sql_query, (current_user["username"],))
        else:
            assignment_logger.warning("Unauthorized attempt to view assignments by user %s", current_user["username"])
            raise HTTPException(status_code=403, detail="You do not have permission to view assignments")

        values = cursor.fetchall()
        result = list_serial(values)
        assignment_logger.info("Assignments retrieved successfully by user %s", current_user["username"])
        return result
    except Exception as e:
        assignment_logger.error("Error retrieving assignments: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@assignment_router.put("/{assignmentId}")
async def update_assignment(assignmentId: str, assigned: bool, current_user: dict = Depends(authenticate_user)):
    """Update the assignment status."""
    try:
        if current_user["role"] != Role.admin:
            assignment_logger.warning("Unauthorized attempt to update assignment %s by user %s", assignmentId, current_user["username"])
            raise HTTPException(status_code=403, detail="Only admin can update assignment status")

        cursor.execute("UPDATE assignment SET assigned = %s WHERE assignmentId = %s;", (assigned, assignmentId))
        cursor.execute("UPDATE employee SET is_assigned = %s WHERE employeeId = (SELECT employeeId FROM assignment WHERE assignmentId = %s);", (assigned, assignmentId))
        sql.commit()
        assignment_logger.info("Assignment %s updated successfully by user %s", assignmentId, current_user["username"])
        return {"message": "Assignment status updated successfully"}
    except Exception as e:
        assignment_logger.error("Error updating assignment %s: %s", assignmentId, str(e))
        raise HTTPException(status_code=500, detail=str(e))

@assignment_router.delete("/{assignmentId}")
async def delete_assignment(assignmentId: str, current_user: dict = Depends(authenticate_user)):
    """Delete an assignment."""
    try:
        if current_user["role"] != Role.admin:
            assignment_logger.warning("Unauthorized attempt to delete assignment %s by user %s", assignmentId, current_user["username"])
            raise HTTPException(status_code=403, detail="Only admin can delete assignments")

        # Get the employeeId before deleting the assignment
        cursor.execute("SELECT employeeId FROM assignment WHERE assignmentId = %s", (assignmentId,))
        employee_id = cursor.fetchone()

        cursor.execute("DELETE FROM assignment WHERE assignmentId = %s;", (assignmentId,))
        if employee_id:
            cursor.execute("UPDATE employee SET is_assigned = 0 WHERE employeeId = %s;", (employee_id[0],))
        sql.commit()
        assignment_logger.info("Assignment %s deleted successfully by user %s", assignmentId, current_user["username"])
        return {"message": "Assignment deleted successfully"}
    except Exception as e:
        assignment_logger.error("Error deleting assignment %s: %s", assignmentId, str(e))
        raise HTTPException(status_code=500, detail=str(e))

