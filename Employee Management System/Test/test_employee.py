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

def test_enter_employee_details():
    # Define the data for the employee details
    data = {
        "employeeId": "EMP009",
        "email": "Aehal.pandey@company.com",
        "name": "Aehal pandey",
        "salary": 110000,
        "role": "Software Engineer"
    }

    # Authenticate to get the token
    token = get_token("admin_user", "admin_password")

    # Make a POST request to the endpoint with the provided data and token
    response = client.post(f"/employees/?username=admin_user&password=admin_password", json=data)
    
    # Assert that the response status code is 200
    assert response.status_code == 200
    assert response.json() == {"message": "Record added successfully"}

def test_get_my_info():
    # Authenticate to get the token
    token = get_token("admin_user", "admin_password")

    # Make a GET request to get employee info with token
    response = client.get("/employees/my_info?username=admin_user&password=admin_password")

    # Assert that the response status code is 200
    assert response.status_code == 200
    print(response.json())

def test_update_employee_name():
    # Define employee ID and updated name
    employee_id = "EMP009"
    updated_name = "Anupam Sharma"

    # Authenticate to get the token
    token = get_token("admin_user", "admin_password")

    # Make a PUT request to update the employee's name with token
    response = client.put(f"/employees/{employee_id}?name={updated_name}&username=admin_user&password=admin_password")

    # Assert that the response status code is 200
    assert response.status_code == 200
    print(response.json())

def test_delete_employee():
    # Define employee ID to be deleted
    employee_id = "EMP009"

    # Authenticate to get the token
    token = get_token("admin_user", "admin_password")

    # Make a DELETE request to delete the employee record with token
    response = client.delete(f"/employees/?employeeId={employee_id}&username=admin_user&password=admin_password")

    # Assert that the response status code is 200
    assert response.status_code == 200
    assert response.json() == {"message": "Record deleted successfully"}
