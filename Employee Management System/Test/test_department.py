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
def test_enter_department_details():
    # Define the data for the department details
    data = {
          "departmentId": "DEPT003",
          "name": "Deployment",
          "managerId": "MGR001"
    }

    # Make a POST request to the endpoint with the provided data
    response = client.post("/departments/", json=data)
    
    # Assert that the response status code is 200
    assert response.status_code == 200
    
    # Assert that the response JSON matches the expected message
    assert response.json() == {"message": "Record added successfully"}

    # Additional checks to verify the record in the database
    # (if applicable, based on the application's design and setup)



def test_update_department_name():
    # Define department ID and updated name
    department_id = "DEPT001"
    updated_name = "Development Department"

    # Make a PUT request to update the department's name
    response = client.put(f"/departments/{department_id}", params={"name": updated_name})

    # Assert that the response status code is 200
    assert response.status_code == 200
    print(response.json())


def test_delete_department():
    # Define department ID to be deleted
    department_id = "DEPT003"

    # Make a DELETE request to delete the department record
    response = client.delete(f"/departments/", params={"departmentId": department_id})

    # Assert that the response status code is 200
    assert response.status_code == 200
    assert response.json() == {"message": "Record deleted successfully"}
