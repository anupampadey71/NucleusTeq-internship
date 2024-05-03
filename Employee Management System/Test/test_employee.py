import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to Python path

from fastapi.testclient import TestClient
from main import app  # Importing from the parent folder

client = TestClient(app)

def test_main():
    response = client.get("/")
    assert response.status_code == 200
    print(response.json())
def test_enter_employee_details():
    # Define the data for the employee details
    data = {
        "employeeId": "EMP009",
        "email": "nehal.pandey@company.com",
        "name": "nehal pandey",
        "salary": 110000,
        "role": "Software Engineer"
    }

    # Make a POST request to the endpoint with the provided data
    response = client.post("/employees/", json=data)
    
    # Assert that the response status code is 200
    assert response.status_code == 200
    
    # Assert that the response JSON matches the expected message
    assert response.json() == {"message": "Record added successfully"}

    # Additional checks to verify the record in the database
    # (if applicable, based on the application's design and setup)



def test_update_employee_name():
    # Define employee ID and updated name
    employee_id = "EMP007"
    updated_name = "Anupam Sharma"

    # Make a PUT request to update the employee's name
    response = client.put(f"/employees/{employee_id}", params={"name": updated_name})

    # Assert that the response status code is 200
    assert response.status_code == 200
    print(response.json())


def test_delete_employee():
    # Define employee ID to be deleted
    employee_id = "EMP007"

    # Make a DELETE request to delete the employee record
    response = client.delete(f"/employees/", params={"employeeId": employee_id})

    # Assert that the response status code is 200
    assert response.status_code == 200
    assert response.json() == {"message": "Record deleted successfully"}
