import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to Python path

from fastapi.testclient import TestClient
from main import app  # Importing from the parent folder

client = TestClient(app)

def test_create_project():
    """Tests creating a new project"""
    # Define data for the project
    data = {
        "projectId": "PROJ004",
        "name": "OTT App",
        "description": "Create a mobile app to stream web series"
    }

    # Send POST request to create project
    response = client.post("/project/", json=data)

    # Assert successful creation
    assert response.status_code == 200
    assert response.json() == {"message": "Project added successfully"}


def test_get_all_projects():
    """Tests retrieving all projects"""
    # Send GET request to retrieve all projects
    response = client.get("/project/all_projects")

    # Assert successful retrieval (content will depend on your data)
    assert response.status_code == 200



def test_update_project():
    """Tests updating a project"""
    # Define project ID, updated name, and updated description
    project_id = "PROJ005"
    updated_name = "Pomodoro"
    updated_description = "create a pomodoro project for efficienct time management"

    # Send PUT request to update project
    response = client.put(f"/project/{project_id}", params={"name": updated_name, "description": updated_description})

    # Assert successful update
    assert response.status_code == 200
    assert response.json() == {"message": "Project updated successfully"}


def test_delete_project():
    """Tests deleting a project"""
    # Define project ID to delete
    project_id = "PROJ005"  # Assuming PROJ004 was created in test_create_project

    # Send DELETE request to delete the project
    response = client.delete(f"/project/{project_id}")

    # Assert successful deletion
    assert response.status_code == 200
    assert response.json() == {"message": "Project deleted successfully"}
