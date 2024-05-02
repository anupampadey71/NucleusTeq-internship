from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_main():
    response = client.get("/")
    assert response.status_code == 200
    print(response.json())
def test_enter_employee_details():
    # Define the data for the employee details
    data = {
        "employeeId": "EMP006",
        "email": "nehal.pandey@company.com",
        "name": "nehal pandey",
        "salary": "110000",
        "role": "Software Engineer"
    }

    # Make a POST request to the endpoint with the provided data
    response = client.post("/", json=data)
    
    # Assert that the response status code is 200
    assert response.status_code == 200
    
    # Assert that the response JSON matches the expected message
    assert response.json() == {"message": "Record added successfully"}

    # Additional checks to verify the record in the database
    # (if applicable, based on the application's design and setup)


def test_update_name():
    response = client.put("/EMP005", params={"name": "ricky"})
    assert response.status_code == 200
    print(response.json())

def test_delete():
    response = client.delete("/", params={"employeeId": "EMP006"})
    assert response.status_code == 200
    print(response.json())
