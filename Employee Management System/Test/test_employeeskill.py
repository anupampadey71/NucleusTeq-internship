import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to Python path

from fastapi.testclient import TestClient
from main import app  # Importing from the parent folder

client = TestClient(app)


def test_create_employee_skill():
    """Tests creating a new employee skill association"""
    # Define data for the employee skill association
    data = {
        "employeeId": "EMP005",
        "skillId": "SKILL002"
    }

    # Send POST request to create employee skill association
    response = client.post("/employeeskill/", json=data)

    # Assert successful creation
    assert response.status_code == 200
    assert response.json() == {"message": "Employee skill association added successfully"}


def test_update_employee_skill():
    """Tests updating an employee's skill"""
    # Define query parameters
    params = {
        "employee_id": "EMP002",
        "current_skill_id": "SKILL002",
        "new_skill_id": "SKILL003"
    }

    # Send PUT request to update employee skill
    response = client.put("/employeeskill/", params=params)

    # Assert successful update
    assert response.status_code == 200
    assert response.json() == {"message": "Employee skill association updated successfully for employee EMP002"}



def test_get_employee_skills():
    """Tests retrieving skills of a specific employee"""
    # Define employee ID
    employee_id = "EMP001"

    # Send GET request to retrieve skills of the employee
    response = client.get(f"/employeeskill/{employee_id}")

    # Assert successful retrieval (content will depend on your data)
    assert response.status_code == 200


def test_delete_employee_skill():
    """Tests deleting an employee's skill"""
    # Define employee ID and skill ID to delete
    employee_id = "EMP005"
    skill_id = "SKILL001"

    # Send DELETE request to delete the employee's skill
    response = client.delete(f"/employeeskill/{employee_id}/{skill_id}")

    # Assert successful deletion
    assert response.status_code == 200
    assert response.json() == {"message": "Employee skill association deleted successfully"}
