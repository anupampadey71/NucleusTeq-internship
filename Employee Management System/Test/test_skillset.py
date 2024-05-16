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
        "skillId": "SKILL005",
        "skillName": "C++ programming"
    }

    # Make a POST request to create employee skill with admin authentication
    response = client.post("/skillsets/", json=data, params={"username": "admin_user", "password": "admin_password"})

    # Assert successful creation
    assert response.status_code == 200
    assert response.json() == {"message": "Skill added successfully"}

def test_get_all_skills():
    """Tests retrieving all skills"""
    # Make a GET request to retrieve all skills with admin authentication
    response = client.get("/skillsets/all_skills", params={"username": "admin_user", "password": "admin_password"})

    # Assert successful retrieval (content will depend on your data)
    assert response.status_code == 200

def test_update_skill_name():
    """Tests updating a skill name"""
    # Make a PUT request to update skill name with admin authentication
    response = client.put("/skillsets/SKILL005", params={"name": "C programming", "username": "admin_user", "password": "admin_password"})

    # Assert successful update
    assert response.status_code == 200
    assert response.json() == {"message": "Skill name updated successfully"}

def test_delete_skill():
    """Tests deleting a skill"""
    # Make a DELETE request to delete a skill with admin authentication
    response = client.delete("/skillsets/SKILL005", params={"username": "admin_user", "password": "admin_password"})

    # Assert successful deletion
    assert response.status_code == 200
    assert response.json() == {"message": "Skill deleted successfully"}
