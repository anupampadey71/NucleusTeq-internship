import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to Python path

from fastapi.testclient import TestClient
from main import app  # Importing from the parent folder

client = TestClient(app)

# Function to get authentication token
def get_token(username, password):
    response = client.post("/auth/login", data={"username": username, "password": password})
    return response.json()["token"]

def test_create_employee_skill():
    """Tests creating a new employee skill association"""
    # Define data for the employee skill association
    data = {
        "employeeId": "EMP001",
        "skillId": "SKILL003"
    }

    # Authenticate to get the token
    token = get_token("EMP001", "EMP001")

    # Send POST request to create employee skill association
    response = client.post("/employeeskill/", 
                           params={"username": "EMP001", "password": "EMP001"},
                           json=data,
                           headers={"Authorization": f"Bearer {token}", "accept": "application/json", "Content-Type": "application/json"})

    # Assert successful creation
    assert response.status_code == 200
    assert response.json() == {"message": "Employee skill association added successfully"}


def test_update_employee_skill():
    """Tests updating an employee's skill"""
    # Authenticate to get the token
    token = get_token("EMP001", "EMP001")

    # Send PUT request to update employee skill
    response = client.put("/employeeskill/", 
                          params={"employee_id": "EMP001", "current_skill_id": "SKILL003", "new_skill_id": "SKILL004", "username": "EMP001", "password": "EMP001"},
                          headers={"Authorization": f"Bearer {token}", "accept": "application/json"})

    # Assert successful update
    assert response.status_code == 200
    assert response.json() == {"message": "Employee skill association updated successfully for employee EMP001"}


def test_get_employee_skills():
    """Tests retrieving skills of a specific employee"""
    # Authenticate to get the token
    token = get_token("EMP001", "EMP001")

    # Send GET request to retrieve skills of the employee
    response = client.get("/employeeskill/EMP001", 
                          params={"username": "EMP001", "password": "EMP001"},
                          headers={"Authorization": f"Bearer {token}", "accept": "application/json"})

    # Assert successful retrieval
    assert response.status_code == 200


def test_delete_employee_skill():
    """Tests deleting an employee's skill"""
    # Authenticate to get the token
    token = get_token("EMP001", "EMP001")

    # Send DELETE request to delete the employee's skill
    response = client.delete("/employeeskill/EMP001/SKILL004", 
                             params={"username": "EMP001", "password": "EMP001"},
                             headers={"Authorization": f"Bearer {token}", "accept": "application/json"})

    # Assert successful deletion
    assert response.status_code == 200
    assert response.json() == {"message": "Employee skill association deleted successfully"}