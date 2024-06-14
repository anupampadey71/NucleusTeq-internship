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
          "departmentId": "DEPT004",
          "name": "Deployment",
          "managerId": "MGR002"
    }

    # Authenticate to get the token
    token = get_token("ADM001", "ADM001")

    # Make a POST request to the endpoint with the provided data and token
    response = client.post("/departments/", json=data, params={"username": "ADM001", "password": "ADM001"})
    
    # Assert that the response status code is 200
    assert response.status_code == 200
    
    # Assert that the response JSON matches the expected message
    assert response.json() == {"message": "Record added successfully"}

def test_update_department_name():
    # Define department ID and updated name
    department_id = "DEPT004"
    updated_name = "Testing Department"

    # Authenticate to get the token
    token = get_token("ADM001", "ADM001")

    # Make a PUT request to update the department's name with token
    response = client.put(f"/departments/{department_id}", params={"name": updated_name, "username": "ADM001", "password": "ADM001"})

    # Assert that the response status code is 200
    assert response.status_code == 200
    print(response.json())

def test_delete_department():
    # Define department ID to be deleted
    department_id = "DEPT004"

    # Authenticate to get the token
    token = get_token("ADM001", "ADM001")

    # Make a DELETE request to delete the department record with token
    response = client.delete("/departments/", params={"departmentId": department_id, "username": "ADM001", "password": "ADM001"})

    # Assert that the response status code is 200
    assert response.status_code == 200
    assert response.json() == {"message": "Record deleted successfully"}

def test_admin_get_my_info():
    # Authenticate to get the token
    token = get_token("ADM001", "ADM001")

    # Make a GET request to the my_info endpoint with the token
    response = client.get("/departments/my_info", params={"username": "ADM001", "password": "ADM001"})

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Print the response JSON for verification
    print(response.json())

def test_manager_get_my_info():
    # Authenticate to get the token
    token = get_token("ADM001", "ADM001")

    # Make a GET request to the my_info endpoint with the token
    response = client.get("/departments/my_info", params={"username": "MGR001", "password": "MGR001"})

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Print the response JSON for verification
    print(response.json())

def test_user_get_my_info():
    # Authenticate to get the token
    token = get_token("ADM001", "ADM001")

    # Make a GET request to the my_info endpoint with the token
    response = client.get("/departments/my_info", params={"username": "EMP001", "password": "EMP001"})

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Print the response JSON for verification
    print(response.json())

#negative test cases
def test_negative_enter_department_details():
    # Define the data for the department details
    data = {
          "departmentId": "DEPT004",
          "name": "Deployment",
          "managerId": "MGR002"
    }

    # Authenticate to get the token
    token = get_token("EMP001", "EMP001")

    # Make a POST request to the endpoint with the provided data and token
    response = client.post("/departments/", json=data, params={"username": "EMP001", "password": "EMP001"})
    
    # Assert that the response status code is 403
    assert response.status_code == 403
    
    # Assert that the response JSON matches the expected message
    assert response.json() == {"detail":"Only admin can add new departments"}

def test_negative_update_department_name():
    # Define department ID and updated name
    department_id = "DEPT003"
    updated_name = "Testing Department"

    # Authenticate to get the token
    token = get_token("EMP001", "EMP001")

    # Make a PUT request to update the department's name with token
    response = client.put(f"/departments/{department_id}", params={"name": updated_name, "username": "EMP001", "password": "EMP001"})

     # Assert that the response status code is 403
    assert response.status_code == 403
    assert response.json() == {"detail":"Only admin can update department details"}

def test_negative_delete_department():
    # Define department ID to be deleted
    department_id = "DEPT004"

    # Authenticate to get the token
    token = get_token("EMP001", "EMP001")

    # Make a DELETE request to delete the department record with token
    response = client.delete("/departments/", params={"departmentId": department_id, "username": "EMP001", "password": "EMP001"})

    # Assert that the response status code is 403
    assert response.status_code == 403
    assert response.json() == {"detail":"Only admin can delete department records"}