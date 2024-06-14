import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to Python path

from fastapi.testclient import TestClient
from main import app  # Importing from the parent folder

client = TestClient(app)

# Function to get authentication token
def get_token(username, password):
    response = client.post("/auth/login", data={"username": username, "password": password})
    response_data = response.json()
    if response.status_code == 200 and "token" in response_data:
        return response_data["token"]
    else:
        print(f"Error obtaining token for {username}: {response_data}")
        return None

def test_user_create_employee_skill():
    """Tests creating a new employee skill association"""
    data = {
        "employeeId": "EMP001",
        "skillId": "SKILL004"
    }

    token = get_token("EMP001", "EMP001")
    assert token is not None

    response = client.post("/employeeskill/", 
                           params={"username": "EMP001", "password": "EMP001"},
                           json=data,
                           headers={"Authorization": f"Bearer {token}", "accept": "application/json", "Content-Type": "application/json"})

    assert response.status_code == 200
    assert response.json() == {"message": "Employee skill association added successfully"}

def test_admin_create_employee_skill():
    """Tests creating a new employee skill association"""
    data = {
        "employeeId": "EMP001",
        "skillId": "SKILL005"
    }

    token = get_token("ADM001", "ADM001")
    assert token is not None

    response = client.post("/employeeskill/", 
                           params={"username": "ADM001", "password": "ADM001"},
                           json=data,
                           headers={"Authorization": f"Bearer {token}", "accept": "application/json", "Content-Type": "application/json"})

    assert response.status_code == 200
    assert response.json() == {"message": "Employee skill association added successfully"}

def test_user_update_employee_skill():
    """Tests updating an employee's skill"""
    token = get_token("EMP001", "EMP001")
    assert token is not None

    response = client.put("/employeeskill/", 
                          params={"employee_id": "EMP001", "current_skill_id": "SKILL004", "new_skill_id": "SKILL006", "username": "EMP001", "password": "EMP001"},
                          headers={"Authorization": f"Bearer {token}", "accept": "application/json"})

    assert response.status_code == 200
    assert response.json() == {"message": "Employee skill association updated successfully for employee EMP001"}

def test_admin_update_employee_skill():
    """Tests updating an employee's skill"""
    token = get_token("ADM001", "ADM001")
    assert token is not None

    response = client.put("/employeeskill/", 
                          params={"employee_id": "EMP001", "current_skill_id": "SKILL006", "new_skill_id": "SKILL004", "username": "ADM001", "password": "ADM001"},
                          headers={"Authorization": f"Bearer {token}", "accept": "application/json"})

    assert response.status_code == 200
    assert response.json() == {"message": "Employee skill association updated successfully for employee EMP001"}

def test_user_get_employee_skills():
    """Tests retrieving skills of a specific employee"""
    token = get_token("EMP001", "EMP001")
    assert token is not None

    response = client.get("/employeeskill/EMP001", 
                          params={"username": "EMP001", "password": "EMP001"},
                          headers={"Authorization": f"Bearer {token}", "accept": "application/json"})

    assert response.status_code == 200

def test_manager_get_employee_skills():
    """Tests retrieving skills of a specific employee"""
    token = get_token("MGR001", "MGR001")
    assert token is not None

    response = client.get("/employeeskill/EMP001", 
                          params={"username": "MGR001", "password": "MGR001"},
                          headers={"Authorization": f"Bearer {token}", "accept": "application/json"})

    assert response.status_code == 200

def test_admin_get_employee_skills():
    """Tests retrieving skills of a specific employee"""
    token = get_token("ADM001", "ADM001")
    assert token is not None

    response = client.get("/employeeskill/EMP001", 
                          params={"username": "ADM001", "password": "ADM001"},
                          headers={"Authorization": f"Bearer {token}", "accept": "application/json"})

    assert response.status_code == 200

def test_user_delete_employee_skill():
    """Tests deleting an employee's skill"""
    token = get_token("EMP001", "EMP001")
    assert token is not None

    response = client.delete("/employeeskill/EMP001/SKILL005", 
                             params={"username": "EMP001", "password": "EMP001"},
                             headers={"Authorization": f"Bearer {token}", "accept": "application/json"})

    assert response.status_code == 200
    assert response.json() == {"message": "Employee skill association deleted successfully"}

def test_admin_delete_employee_skill():
    """Tests deleting an employee's skill"""
    token = get_token("ADM001", "ADM001")
    assert token is not None

    response = client.delete("/employeeskill/EMP001/SKILL004", 
                             params={"username": "ADM001", "password": "ADM001"},
                             headers={"Authorization": f"Bearer {token}", "accept": "application/json"})

    assert response.status_code == 200
    assert response.json() == {"message": "Employee skill association deleted successfully"}


#negative test cases
def test_user_negative_create_employee_skill():
    """Tests creating a new employee skill association"""
    data = {
        "employeeId": "EMP002",
        "skillId": "SKILL001"
    }

    token = get_token("EMP003", "EMP003")
    assert token is not None

    response = client.post("/employeeskill/", 
                           params={"username": "EMP003", "password": "EMP003"},
                           json=data,
                           headers={"Authorization": f"Bearer {token}", "accept": "application/json", "Content-Type": "application/json"})

    assert response.status_code == 403
    assert response.json() == {"detail": "Users can only add skills for themselves"} 

def test_manager_negative_create_employee_skill():
    """Tests creating a new employee skill association"""
    data = {
        "employeeId": "EMP002",
        "skillId": "SKILL001"
    }

    token = get_token("MGR001", "MGR001")
    assert token is not None

    response = client.post("/employeeskill/", 
                           params={"username": "MGR001", "password": "MGR001"},
                           json=data,
                           headers={"Authorization": f"Bearer {token}", "accept": "application/json", "Content-Type": "application/json"})

    assert response.status_code == 403
    assert response.json() == {"detail": "Only admin or user can add employee skills"} 


def test_user_negative_update_employee_skill():
    """Tests updating an employee's skill"""
    token = get_token("EMP001", "EMP001")
    assert token is not None

    response = client.put("/employeeskill/", 
                          params={"employee_id": "EMP002", "current_skill_id": "SKILL002", "new_skill_id": "SKILL001", "username": "EMP001", "password": "EMP001"},
                          headers={"Authorization": f"Bearer {token}", "accept": "application/json"})

    assert response.status_code == 403
    assert response.json() == {"detail": "Users can only update their own skills"}

def test_manager_negative_update_employee_skill():
    """Tests updating an employee's skill"""
    token = get_token("MGR001", "MGR001")
    assert token is not None

    response = client.put("/employeeskill/", 
                          params={"employee_id": "EMP002", "current_skill_id": "SKILL002", "new_skill_id": "SKILL001", "username": "MGR001", "password": "MGR001"},
                          headers={"Authorization": f"Bearer {token}", "accept": "application/json"})

    assert response.status_code == 403
    assert response.json() == {"detail": "Only admin or user can update employee skills"}

def test_user_negative_delete_employee_skill():
    """Tests deleting an employee's skill"""
    token = get_token("EMP001", "EMP001")
    assert token is not None

    response = client.delete("/employeeskill/EMP002/SKILL002", 
                             params={"username": "EMP001", "password": "EMP001"},
                             headers={"Authorization": f"Bearer {token}", "accept": "application/json"})

    assert response.status_code == 403
    assert response.json() == {"detail": "Users can only delete their own skills"}

def test_manager_negative_delete_employee_skill():
    """Tests deleting an employee's skill"""
    token = get_token("MGR002", "MGR002")
    assert token is not None

    response = client.delete("/employeeskill/EMP002/SKILL002", 
                             params={"username": "MGR002", "password": "MGR002"},
                             headers={"Authorization": f"Bearer {token}", "accept": "application/json"})

    assert response.status_code == 403
    assert response.json() == {"detail": "Only admin or user can delete employee skills"}


