from fastapi import APIRouter, HTTPException, Depends
from config.databases import sql, cursor
from model.assignment_models import Register, create_assignment
from schema.assignment_schema import list_serial
from .auth_route import authenticate_user, Role

assignment_router = APIRouter()

def is_employee_available(employee_id: str, skill_id: str, project_id: str) -> bool:
    """Check if the employee has the required skill for the project."""
    sql_query = "SELECT COUNT(*) FROM employeeskill WHERE employeeId = %s AND skillId = %s;"
    cursor.execute(sql_query, (employee_id, skill_id))
    result = cursor.fetchone()
    return result[0] > 0

@assignment_router.post("/")
async def create_assignment(assignment: create_assignment, current_user: dict = Depends(authenticate_user)):
    """Create a new assignment."""
    if current_user["role"] != Role.admin:
        raise HTTPException(status_code=403, detail="Only admin can create assignments")

    # Check if request status is 'Open'
    cursor.execute("SELECT status FROM request WHERE requestId = %s", (assignment.requestId,))
    request_status = cursor.fetchone()
    if not request_status or request_status[0] != 'Open':
        raise HTTPException(status_code=400, detail="Request is not open")

    # Check if the employee is available
    cursor.execute("SELECT is_assigned FROM employee WHERE employeeId = %s", (assignment.employeeId,))
    employee_status = cursor.fetchone()
    if not employee_status or employee_status[0] != 0:
        raise HTTPException(status_code=400, detail="Employee is not available")

    # Check if the employee has the required skill
    cursor.execute("SELECT skillId FROM employeeskill WHERE employeeId = %s", (assignment.employeeId,))
    employee_skills = cursor.fetchall()
    cursor.execute("SELECT skillId FROM request WHERE requestId = %s", (assignment.requestId,))
    required_skill = cursor.fetchone()
    
    # Extract the required skill ID
    required_skill_id = required_skill[0] if required_skill else None
    if required_skill_id not in [skill[0] for skill in employee_skills]:
        raise HTTPException(status_code=400, detail="Employee does not have the required skill")

    # Insert the assignment
    try:
        cursor.execute("INSERT INTO assignment (assignmentId, requestId, employeeId, projectId, assigned) VALUES (%s, %s, %s, %s, %s)", 
                       (assignment.assignmentId, assignment.requestId, assignment.employeeId, assignment.projectId, False))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Assignment added successfully"}


@assignment_router.get("/all_assignments")
async def get_all_assignments(current_user: dict = Depends(authenticate_user)):
    """Retrieve all assignments."""
    if current_user["role"] == Role.admin:
        sql_query = "SELECT * FROM assignment;"
        cursor.execute(sql_query)
    elif current_user["role"] == Role.user:
        sql_query = "SELECT * FROM assignment WHERE employeeId = %s;"
        cursor.execute(sql_query, (current_user["username"],))
    elif current_user["role"] == Role.manager:
        sql_query = """
            SELECT a.*
            FROM assignment a
            JOIN project p ON a.projectId = p.projectId
            WHERE p.managerId = %s;
        """
        cursor.execute(sql_query, (current_user["username"],))
    else:
        raise HTTPException(status_code=403, detail="You do not have permission to view assignments")

    try:
        values = cursor.fetchall()
        result = list_serial(values)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result

@assignment_router.put("/{assignmentId}")
async def update_assignment(assignmentId: str, assigned: bool, current_user: dict = Depends(authenticate_user)):
    """Update the assignment status."""
    if current_user["role"] != Role.admin:
        raise HTTPException(status_code=403, detail="Only admin can update assignment status")

    try:
        cursor.execute("UPDATE assignment SET assigned = %s WHERE assignmentId = %s;", (assigned, assignmentId))
        cursor.execute("UPDATE employee SET is_assigned = %s WHERE employeeId = (SELECT employeeId FROM assignment WHERE assignmentId = %s);", (assigned, assignmentId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Assignment status updated successfully"}

@assignment_router.delete("/{assignmentId}")
async def delete_assignment(assignmentId: str, current_user: dict = Depends(authenticate_user)):
    """Delete an assignment."""
    if current_user["role"] != Role.admin:
        raise HTTPException(status_code=403, detail="Only admin can delete assignments")

    try:
        # Get the employeeId before deleting the assignment
        cursor.execute("SELECT employeeId FROM assignment WHERE assignmentId = %s", (assignmentId,))
        employee_id = cursor.fetchone()

        cursor.execute("DELETE FROM assignment WHERE assignmentId = %s;", (assignmentId,))
        if employee_id:
            cursor.execute("UPDATE employee SET is_assigned = 0 WHERE employeeId = %s;", (employee_id[0],))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Assignment deleted successfully"}
