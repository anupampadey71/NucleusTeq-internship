import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to Python path

from fastapi.testclient import TestClient
from main import app  # Importing from the parent folder

client = TestClient(app)

def test_create_manager():
    """Tests creating a new manager"""
    # Define data for the manager
    data = {
        "managerId": "MGR004",
        "employeeId": "EMP002"
    }

    # Send POST request to create manager
    response = client.post("/manager/", json=data)

    # Assert successful creation
    assert response.status_code == 200
    assert response.json() == {"message": "Manager added successfully"}


def test_get_all_managers():
    """Tests retrieving all managers"""
    # Send GET request to retrieve all managers
    response = client.get("/manager/")

    # Assert successful retrieval (content will depend on your data)
    assert response.status_code == 200


def test_update_manager():
    """Tests updating a manager"""
    # Define manager ID and updated employee ID
    manager_id = "MGR0004"
    updated_employee_id = "EMP001"

    # Send PUT request to update manager
    response = client.put(f"/manager/{manager_id}", params={"employeeId": updated_employee_id})

    # Assert successful update
    assert response.status_code == 200
    assert response.json() == {"message": "Manager updated successfully"}



def test_delete_manager():
    """Tests deleting a manager"""
    # Define manager ID to delete
    manager_id = "MGR004"  # Assuming MGR003 was created in test_create_manager

    # Send DELETE request to delete the manager
    response = client.delete(f"/manager/{manager_id}")

    # Assert successful deletion
    assert response.status_code == 200
    assert response.json() == {"message": "Manager deleted successfully"}

