import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to Python path
import requests
from fastapi.testclient import TestClient
from main import app  # Importing from the parent folder

client = TestClient(app)

# Function to get authentication token
def get_token(username, password):
    response = client.post("/auth/login", data={"username": username, "password": password})
    return response.json()["token"]

def test_main():
    response = client.get("/")
    assert response.status_code == 200
    print(response.json())

def test_admin_create_project():
    """Tests creating a new project"""
    # Define data for the project
    data = {
        "projectId": "PROJ005",
        "name": "OTT App",
        "description": "Create a mobile app to stream web series",
        "managerId": "MGR001"
    }

    # Authenticate as admin to get the token
    token = get_token("ADM001", "ADM001")

    # Send POST request to create project
    response = client.post("/project/?username=ADM001&password=ADM001", json=data, headers={"Authorization": f"Bearer {token}"})

    # Assert successful creation
    assert response.status_code == 200
    assert response.json() == {"message": "Project added successfully"}

def test_manager_create_project():
    """Tests creating a new project"""
    # Define data for the project
    data = {
        "projectId": "PROJ006",
        "name": "Youtube school App",
        "description": "Create a mobile app to stream school lectures",
        "managerId": "MGR001"
    }

    # Authenticate as admin to get the token
    token = get_token("MGR001", "MGR001")

    # Send POST request to create project
    response = client.post("/project/?username=MGR001&password=MGR001", json=data, headers={"Authorization": f"Bearer {token}"})

    # Assert successful creation
    assert response.status_code == 200
    assert response.json() == {"message": "Project added successfully"}


def test_admin_get_all_projects():
    """Tests retrieving all projects"""
    # Authenticate to get the token
    token = get_token("ADM001", "ADM001")

    # Send GET request to retrieve all projects
    response = client.get("/project/all_projects?username=ADM001&password=ADM001", headers={"Authorization": f"Bearer {token}"})

    # Assert successful retrieval (content will depend on your data)
    assert response.status_code == 200

def test_manager_get_all_projects():
    """Tests retrieving all projects"""
    # Authenticate to get the token
    token = get_token("MGR001", "MGR001")

    # Send GET request to retrieve all projects
    response = client.get("/project/all_projects?username=MGR001&password=MGR001", headers={"Authorization": f"Bearer {token}"})

    # Assert successful retrieval (content will depend on your data)
    assert response.status_code == 200

def test_user_get_all_projects():
    """Tests retrieving all projects"""
    # Authenticate to get the token
    token = get_token("EMP001", "EMP001")

    # Send GET request to retrieve all projects
    response = client.get("/project/all_projects?username=EMP001&password=EMP001", headers={"Authorization": f"Bearer {token}"})

    # Assert successful retrieval (content will depend on your data)
    assert response.status_code == 200


def test_admin_update_project():
    # Define project ID and updated details
    project_id = "PROJ005"
    updated_details = {
        "name": "Habit Tracker",
        "description": "To Track your daily habits",
        "managerId": "MGR001"
    }

    # Authenticate to get the token
    token = get_token("ADM001", "ADM001")

    # Construct the request URL with query parameters
    url = f"/project/{project_id}?username=ADM001&password=ADM001"

    # Make a PUT request to update the project details with the token
    response = client.put(
        url,
        json=updated_details,
        headers={"Authorization": f"Bearer {token}", "accept": "application/json", "Content-Type": "application/json"}
    )

    # Print response details for debugging
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")

    # Assert that the response status code is 200
    assert response.status_code == 200
    assert response.json() == {"message": "Project updated successfully"}

def test_manager_update_project():
    # Define project ID and updated details
    project_id = "PROJ006"
    updated_details = {
        "name": "Water Tracker",
        "description": "To Track your daily water intake",
        "managerId": "MGR001"
    }

    # Authenticate to get the token
    token = get_token("ADM001", "ADM001")

    # Construct the request URL with query parameters
    url = f"/project/{project_id}?username=ADM001&password=ADM001"

    # Make a PUT request to update the project details with the token
    response = client.put(
        url,
        json=updated_details,
        headers={"Authorization": f"Bearer {token}", "accept": "application/json", "Content-Type": "application/json"}
    )

    # Print response details for debugging
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")

    # Assert that the response status code is 200
    assert response.status_code == 200
    assert response.json() == {"message": "Project updated successfully"}
    
def test_admin_delete_project():
    """Tests deleting a project"""
    # Define project ID to delete
    project_id = "PROJ005"

    # Authenticate as admin to get the token
    token = get_token("ADM001", "ADM001")

    # Send DELETE request to delete the project
    response = client.delete(f"/project/{project_id}?username=ADM001&password=ADM001", headers={"Authorization": f"Bearer {token}"})

    # Assert successful deletion
    assert response.status_code == 200
    assert response.json() == {"message": "Project deleted successfully"}

def test_manager_delete_project():
    """Tests deleting a project"""
    # Define project ID to delete
    project_id = "PROJ006"

    # Authenticate as admin to get the token
    token = get_token("MGR001", "MGR001")

    # Send DELETE request to delete the project
    response = client.delete(f"/project/{project_id}?username=MGR001&password=MGR001", headers={"Authorization": f"Bearer {token}"})

    # Assert successful deletion
    assert response.status_code == 200
    assert response.json() == {"message": "Project deleted successfully"}
