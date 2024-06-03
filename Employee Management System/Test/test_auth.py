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

def test_admin_login():
    response = client.post("/auth/login", data={"username": "ADM001", "password": "ADM001"})
    assert response.status_code == 200
    assert "token" in response.json()
    assert "username" in response.json()
    assert "role" in response.json()
    assert "password" in response.json()

def test_manager_login():
    response = client.post("/auth/login", data={"username": "MGR001", "password": "MGR001"})
    assert response.status_code == 200
    assert "token" in response.json()
    assert "username" in response.json()
    assert "role" in response.json()
    assert "password" in response.json()


def test_user_login():
    response = client.post("/auth/login", data={"username": "EMP001", "password": "EMP001"})
    assert response.status_code == 200
    assert "token" in response.json()
    assert "username" in response.json()
    assert "role" in response.json()
    assert "password" in response.json()


def test_change_password():
    # Authenticate to get the token
    token = get_token("EMP002", "EMP002")

    # Make a PUT request to change the password
    response = client.put("/auth/change-password", 
                           data={"username": "EMP002", "old_password": "EMP002", "new_password": "password"})
    
    # Assert that the response status code is 200
    assert response.status_code == 200
    assert response.json() == {"message": "Password updated successfully"}


