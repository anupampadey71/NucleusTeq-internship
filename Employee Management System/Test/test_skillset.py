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
    """Tests creating a new employee skill"""
    # Define data for the employee skill association
    data = {
        "skillId": "SKILL007",
        "skillName": "javascript"
    }

    # Make a POST request to create employee skill with admin authentication
    response = client.post("/skillsets/", json=data, params={"username": "ADM001", "password": "ADM001"})

    # Assert successful creation
    assert response.status_code == 200
    assert response.json() == {"message": "Skill added successfully"}

def test_admin_get_all_skills():
    """Tests retrieving all skills"""
    # Make a GET request to retrieve all skills with admin authentication
    response = client.get("/skillsets/all_skills", params={"username": "ADM001", "password": "ADM001"})

    # Assert successful retrieval (content will depend on your data)
    assert response.status_code == 200

def test_manager_get_all_skills():
    """Tests retrieving all skills"""
    # Make a GET request to retrieve all skills with admin authentication
    response = client.get("/skillsets/all_skills", params={"username": "MGR001", "password": "MGR001"})

    # Assert successful retrieval (content will depend on your data)
    assert response.status_code == 200

def test_user_get_all_skills():
    """Tests retrieving all skills"""
    # Make a GET request to retrieve all skills with admin authentication
    response = client.get("/skillsets/all_skills", params={"username": "EMP001", "password": "EMP001"})

    # Assert successful retrieval (content will depend on your data)
    assert response.status_code == 200

def test_update_skill_name():
    """Tests updating a skill name"""
    # Make a PUT request to update skill name with admin authentication
    response = client.put("/skillsets/SKILL007", params={"name": "R programming", "username": "ADM001", "password": "ADM001"})

    # Assert successful update
    assert response.status_code == 200
    assert response.json() == {"message": "Skill name updated successfully"}

def test_delete_skill():
    """Tests deleting a skill"""
    # Make a DELETE request to delete a skill with admin authentication
    response = client.delete("/skillsets/SKILL007", params={"username": "ADM001", "password": "ADM001"})

    # Assert successful deletion
    assert response.status_code == 200
    assert response.json() == {"message": "Skill deleted successfully"}
