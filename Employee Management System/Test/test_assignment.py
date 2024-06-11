import sys
import os
from fastapi.testclient import TestClient
from main import app

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

client = TestClient(app)

def test_create_assignment():
    """Test creating a new assignment"""
    # Define data for the assignment
    data = {
        "assignmentId": "ASSG003",
        "requestId": "REQ004",
        "employeeId": "EMP004",
        "projectId": "PROJ004"
    }

    # Send POST request to create assignment
    response = client.post("/assignment/", params={"username": "ADM001", "password": "ADM001"}, json=data)

    # Assert successful creation
    assert response.status_code == 200
    assert response.json() == {"message": "Assignment added successfully"}

def test_admin_get_all_assignments():
    """Test retrieving all assignments"""
    # Send GET request to retrieve all assignments
    response = client.get("/assignment/all_assignments", params={"username": "ADM001", "password": "ADM001"})

    # Assert successful retrieval
    assert response.status_code == 200
    assert len(response.json()) >= 1  # Assuming there's at least one assignment in the database
def test_user_get_all_assignments():
    """Test retrieving all assignments"""
    # Send GET request to retrieve all assignments
    response = client.get("/assignment/all_assignments", params={"username": "EMP001", "password": "EMP001"})

    # Assert successful retrieval
    assert response.status_code == 200
    assert len(response.json()) >= 1  # Assuming there's at least one assignment in the database

def test_manager_get_all_assignments():
    """Test retrieving all assignments"""
    # Send GET request to retrieve all assignments
    response = client.get("/assignment/all_assignments", params={"username": "MGR001", "password": "MGR001"})

    # Assert successful retrieval
    assert response.status_code == 200
    assert len(response.json()) >= 1  # Assuming there's at least one assignment in the database


def test_update_assignment():
    """Test updating an assignment"""
    # Define assignment ID and updated status
    assignment_id = "ASSG003"
    updated_status = True

    # Send PUT request to update assignment
    response = client.put(f"/assignment/{assignment_id}", params={"assigned": updated_status, "username": "ADM001", "password": "ADM001"})

    # Assert successful update
    assert response.status_code == 200
    assert response.json() == {"message": "Assignment status updated successfully"}


def test_delete_assignment():
    """Test deleting an assignment"""
    # Define assignment ID to delete
    assignment_id = "ASSG003"

    # Send DELETE request to delete the assignment
    response = client.delete(f"/assignment/{assignment_id}", params={"username": "ADM001", "password": "ADM001"})

    # Assert successful deletion
    assert response.status_code == 200
    assert response.json() == {"message": "Assignment deleted successfully"}