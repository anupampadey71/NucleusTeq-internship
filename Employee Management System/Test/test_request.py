import sys
import os
from fastapi.testclient import TestClient
from main import app  # Importing from the parent folder

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to Python path

client = TestClient(app)

def test_create_request():
    """Tests creating a new request"""
    # Define data for the request
    data = {
        "requestId": "REQ001",
        "projectId": "PROJ002",
        "skillId": "SKILL003",
        "status": "Open"
    }

    # Send POST request to create request
    response = client.post("/request/", json=data)

    # Assert successful creation
    assert response.status_code == 200
    assert response.json() == {"message": "Request added successfully"}


def test_get_all_requests():
    """Tests retrieving all requests"""
    # Send GET request to retrieve all requests
    response = client.get("/request/all_requests")

    # Assert successful retrieval (content will depend on your data)
    assert response.status_code == 200


def test_update_request():
    """Tests updating a request"""
    # Define request ID and updated status
    request_id = "REQ001"
    updated_status = "Closed"

    # Send PUT request to update request
    response = client.put(f"/request/{request_id}", params={"status": updated_status})

    # Assert successful update
    assert response.status_code == 200
    assert response.json() == {"message": "Request status updated successfully"}


def test_delete_request():
    """Tests deleting a request"""
    # Define request ID to delete
    request_id = "REQ002"  # Assuming REQ001 was created in test_create_request

    # Send DELETE request to delete the request
    response = client.delete(f"/request/{request_id}")

    # Assert successful deletion
    assert response.status_code == 200
    assert response.json() == {"message": "Request deleted successfully"}
