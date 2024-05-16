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
        "assignmentId": "ASSG004",
        "requestId": "REQ001",
        "employeeId": "EMP001",
        "projectId": "PROJ001",
        "status": "Unassigned"
    }

    # Send POST request to create assignment
    response = client.post("/assignment/", json=data)

    # Assert successful creation
    assert response.status_code == 200
    assert response.json() == {"message": "Assignment added successfully"}


def test_get_all_assignments():
    """Test retrieving all assignments"""
    # Send GET request to retrieve all assignments
    response = client.get("/assignment/all_assignments")

    # Assert successful retrieval (content will depend on your data)
    assert response.status_code == 200
    assert len(response.json()) >= 1  # Assuming there's at least one assignment in the database


def test_update_assignment():
    """Test updating an assignment"""
    # Define assignment ID and updated status
    assignment_id = "ASSG004"
    updated_status = "Assigned"

    # Send PUT request to update assignment
    response = client.put(f"/assignment/{assignment_id}", params={"status": updated_status})

    # Assert successful update
    assert response.status_code == 200
    assert response.json() == {"message": "Assignment status updated successfully"}


def test_delete_assignment():
    """Test deleting an assignment"""
    # Define assignment ID to delete
    assignment_id = "ASSG004"

    # Send DELETE request to delete the assignment
    response = client.delete(f"/assignment/{assignment_id}")

    # Assert successful deletion
    assert response.status_code == 200
    assert response.json() == {"message": "Assignment deleted successfully"}
