import sys
import os
from fastapi.testclient import TestClient
from main import app  # Importing from the parent folder

# Add parent directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

client = TestClient(app)

def get_token(username, password):
    """Function to get authentication token"""
    response = client.post("/auth/login", data={"username": username, "password": password})
    return response.json()["token"]

def test_create_manager():
    """Tests creating a new manager"""
    # Define data for the manager
    data = {
        "managerId": "MGR001",
        "employeeId": "EMP004"
    }

    # Authenticate to get the token
    token = get_token("MGR001", "MGR001")

    # Send POST request to create manager
    response = client.post("/manager/?username=MGR001&password=MGR001", json=data, headers={"Authorization": f"Bearer {token}"})

    # Assert successful creation
    assert response.status_code == 200
    assert response.json() == {"message": "Manager added successfully"}


def test_get_all_managers():
    """Tests retrieving all managers"""
    # Authenticate to get the token
    token = get_token("MGR001", "MGR001")

    # Send GET request to retrieve all managers
    response = client.get("/manager/?username=MGR001&password=MGR001", headers={"Authorization": f"Bearer {token}"})

    # Assert successful retrieval (content will depend on your data)
    assert response.status_code == 200


def test_get_employees_under_manager():
    """Tests retrieving all employees under a manager"""
    # Define manager ID
    manager_id = "MGR001"

    # Authenticate to get the token
    token = get_token("MGR001", "MGR001")

    # Send GET request to retrieve employees under manager MGR001
    response = client.get(f"/manager/{manager_id}/employees?username=MGR001&password=MGR001", headers={"Authorization": f"Bearer {token}"})

    # Assert successful retrieval (content will depend on your data)
    assert response.status_code == 200



def test_update_manager():
    """Tests updating a manager"""
    # Define manager ID and updated employee ID
    manager_id = "MGR001"
    old_employee_id = "EMP004"
    new_employee_id = "EMP003"

    # Authenticate to get the token
    token = get_token("MGR001", "MGR001")

    # Send PUT request to update manager
    response = client.put(f"/manager/{manager_id}?old_employeeId={old_employee_id}&new_employeeId={new_employee_id}&username=MGR001&password=MGR001", headers={"Authorization": f"Bearer {token}"})

    # Assert successful update
    assert response.status_code == 200
    assert response.json() == {"message": "Manager updated successfully"}

def test_delete_manager():
    """Tests deleting a manager"""
    # Define manager ID to delete
    manager_id = "MGR001"
    employee_id = "EMP003"

    # Authenticate to get the token
    token = get_token("MGR001", "MGR001")

    # Send DELETE request to delete the manager
    response = client.delete(f"/manager/{manager_id}?employeeId={employee_id}&username=MGR001&password=MGR001", headers={"Authorization": f"Bearer {token}"})

    # Assert successful deletion
    assert response.status_code == 200
    assert response.json() == {"message": "Manager deleted successfully"}
