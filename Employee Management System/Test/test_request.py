import sys
import os
from fastapi.testclient import TestClient
from main import app  # Importing from the parent folder

# Add parent directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

client = TestClient(app)

# Function to get authentication token
def get_token(username, password):
    response = client.post("/auth/login", data={"username": username, "password": password})
    return response.json()["token"]

def test_create_request():
    """Tests creating a new request"""
    # Define data for the request
    data = {
        "requestId": "REQ006",
        "projectId": "PROJ001",
        "skillId": "SKILL004",
        "status": "Open"
    }

    # Authenticate to get the token
    token = get_token("MGR001", "MGR001")

    # Send POST request to create request
    response = client.post("/request/", 
                           params={"username": "MGR001", "password": "MGR001"},
                           json=data,
                           headers={"Authorization": f"Bearer {token}", "accept": "application/json", "Content-Type": "application/json"})

    # Assert successful creation
    assert response.status_code == 200
    assert response.json() == {"message": "Request added successfully"}


def test_get_all_requests():
    """Tests retrieving all requests"""
    # Authenticate to get the token
    token = get_token("MGR001", "MGR001")

    # Send GET request to retrieve all requests
    response = client.get("/request/all_requests", 
                          params={"username": "MGR001", "password": "MGR001"},
                          headers={"Authorization": f"Bearer {token}", "accept": "application/json"})

    # Assert successful retrieval
    assert response.status_code == 200
    assert "requests" in response.json()


def test_update_request():
    """Tests updating a request"""
    # Authenticate to get the token
    token = get_token("MGR001", "MGR001")

    # Send PUT request to update request
    response = client.put("/request/REQ006", 
                          params={"status": "Closed", "username": "MGR001", "password": "MGR001"},
                          headers={"Authorization": f"Bearer {token}", "accept": "application/json"})

    # Assert successful update
    assert response.status_code == 200
    assert response.json() == {"message": "Request status updated successfully"}


def test_delete_request():
    """Tests deleting a request"""
    # Authenticate to get the token
    token = get_token("MGR001", "MGR001")

    # Send DELETE request to delete the request
    response = client.delete("/request/REQ006", 
                             params={"username": "MGR001", "password": "MGR001"},
                             headers={"Authorization": f"Bearer {token}", "accept": "application/json"})

    # Assert successful deletion
    assert response.status_code == 200
    assert response.json() == {"message": "Request deleted successfully"}
