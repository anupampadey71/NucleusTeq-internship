import sys
import os
from fastapi.testclient import TestClient
from main import app

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to Python path

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
        "employeeId": "EMP007",
        "email": "rashmi.pandey@company.com",
        "name": "rashmi pandey",
        "salary": 100000,
        "role": "Software Engineer"
    }

    # Authenticate to get the token
    token = get_token("ADM001", "ADM001")

    # Make a POST request to the endpoint with the provided data and token
    response = client.post(f"/employees/?username=ADM001&password=ADM001", json=data)
    
    # Assert that the response status code is 200
    assert response.status_code == 200
    assert response.json() == {"message": "Record added successfully"}

def test_admin_get_my_info():
    # Authenticate to get the token
    token = get_token("ADM001", "ADM001")

    # Make a GET request to get employee info with token
    response = client.get("/employees/my_info?username=ADM001&password=ADM001")

    # Assert that the response status code is 200
    assert response.status_code == 200
    print(response.json())

def test_mangaer_get_my_info():
    # Authenticate to get the token
    token = get_token("MGR001", "MGR001")

    # Make a GET request to get employee info with token
    response = client.get("/employees/my_info?username=MGR001&password=MGR001")

    # Assert that the response status code is 200
    assert response.status_code == 200
    print(response.json())

def test_employee_get_my_info():
    # Authenticate to get the token
    token = get_token("EMP001", "EMP001")

    # Make a GET request to get employee info with token
    response = client.get("/employees/my_info?username=EMP001&password=EMP001")

    # Assert that the response status code is 200
    assert response.status_code == 200
    print(response.json())



def test_update_employee_details():
    # Define employee ID and updated details
    employee_id = "EMP007"
    updated_details = {
        "email": "rashmi.tiwari@company.com",
        "name": "rashmi Tiwari",
        "salary": 200000,
        "role": "Senior Software Engineer",
    }

    # Authenticate to get the token
    token = get_token("ADM001", "ADM001")

    # Make a PUT request to update the employee details with token
    response = client.put(f"/employees/{employee_id}?username=ADM001&password=ADM001", json=updated_details)

    # Assert that the response status code is 200
    assert response.status_code == 200
    assert response.json() == {"message": "Record updated successfully"}

def test_delete_employee():
    # Define employee ID to be deleted
    employee_id = "EMP007"

    # Authenticate to get the token
    token = get_token("ADM001", "ADM001")

    # Make a DELETE request to delete the employee record with token
    response = client.delete(f"/employees/?employeeId={employee_id}&username=ADM001&password=ADM001")

    # Assert that the response status code is 200
    assert response.status_code == 200
    assert response.json() == {"message": "Record deleted successfully"}

#negative test cases 
def test_negative_enter_employee_details():
    # Define the data for the employee details
    data = {
        "employeeId": "EMP008",
        "email": "rashmi.pandey@company.com",
        "name": "rashmi pandey",
        "salary": 100000,
        "role": "Software Engineer"
    }

    # Authenticate to get the token
    token = get_token("EMP001", "EMP001")

    # Make a POST request to the endpoint with the provided data and token
    response = client.post(f"/employees/?username=EMP001&password=EMP001", json=data)
    
    # Assert that the response status code is 403
    assert response.status_code == 403
    assert response.json() == {"detail": "Only admin can add new employees"}

def test_negative_delete_employee():
    # Define employee ID to be deleted
    employee_id = "EMP006"

    # Authenticate to get the token
    token = get_token("EMP001", "EMP001")

    # Make a DELETE request to delete the employee record with token
    response = client.delete(f"/employees/?employeeId={employee_id}&username=EMP001&password=EMP001")

    # Assert that the response status code is 200
    assert response.status_code == 403
    assert response.json() == {"detail": "Only admin can delete employee records"}

def test_negative_update_employee_details():
    # Define employee ID and updated details
    employee_id = "EMP006"
    updated_details = {
        "email": "rashmi.tiwari@company.com",
        "name": "rashmi Tiwari",
        "salary": 200000,
        "role": "Senior Software Engineer",
    }

    # Authenticate to get the token
    token = get_token("EMP006", "EMP006")

    # Make a PUT request to update the employee details with token
    response = client.put(f"/employees/{employee_id}?username=EMP006&password=EMP006", json=updated_details)

    # Assert that the response status code is 403
    assert response.status_code == 403
    assert response.json() == {"detail": "Only admin can update employee details"}