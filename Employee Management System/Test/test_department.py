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

def test_main():
    response = client.get("/")
    assert response.status_code == 200
    print(response.json())

def test_enter_department_details():
    # Define the data for the department details
    data = {
          "departmentId": "DEPT003",
          "name": "Deployment",
          "managerId": "MGR002"
    }

    # Authenticate to get the token
    token = get_token("admin_user", "admin_password")

    # Make a POST request to the endpoint with the provided data and token
    response = client.post("/departments/", json=data, params={"username": "admin_user", "password": "admin_password"})
    
    # Assert that the response status code is 200
    assert response.status_code == 200
    
    # Assert that the response JSON matches the expected message
    assert response.json() == {"message": "Record added successfully"}

def test_update_department_name():
    # Define department ID and updated name
    department_id = "DEPT003"
    updated_name = "Testing Department"

    # Authenticate to get the token
    token = get_token("admin_user", "admin_password")

    # Make a PUT request to update the department's name with token
    response = client.put(f"/departments/{department_id}", params={"name": updated_name, "username": "admin_user", "password": "admin_password"})

    # Assert that the response status code is 200
    assert response.status_code == 200
    print(response.json())

def test_delete_department():
    # Define department ID to be deleted
    department_id = "DEPT003"

    # Authenticate to get the token
    token = get_token("admin_user", "admin_password")

    # Make a DELETE request to delete the department record with token
    response = client.delete("/departments/", params={"departmentId": department_id, "username": "admin_user", "password": "admin_password"})

    # Assert that the response status code is 200
    assert response.status_code == 200
    assert response.json() == {"message": "Record deleted successfully"}
