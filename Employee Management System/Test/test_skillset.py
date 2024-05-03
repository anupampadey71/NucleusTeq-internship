import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to Python path

from fastapi.testclient import TestClient
from main import app  # Importing from the parent folder

client = TestClient(app)


def test_create_skillset():
    """Tests creating a new skillset entry"""
    # Define data for the skillset
    data = {
        "skillId": "SKILL005",
        "skillName": "JavaScript Development"
    }

    # Send POST request to create skillset
    response = client.post("/skillsets/", json=data)

    # Assert successful creation
    assert response.status_code == 200
    assert response.json() == {"message": "Skill added successfully"}


def test_get_all_skills():
    """Tests retrieving all skills"""
    # Send GET request to retrieve all skills
    response = client.get("/skillsets/all_skills")

    # Assert successful retrieval (content will depend on your data)
    assert response.status_code == 200


def test_update_skill_name():
    """Tests updating a skill name"""
    # Define skill ID and updated name
    skill_id = "SKILL003"
    updated_name = "Backend Devloper"  # Corrected spelling based on the provided URL

    # Send PUT request to update skill name
    response = client.put(f"/skillsets/{skill_id}", params={"name": updated_name})

    # Assert successful update
    assert response.status_code == 200
    assert response.json() == {"message": "Skill name updated successfully"}



def test_delete_skill():
    """Tests deleting a skill"""
    # Define skill ID to delete
    skill_id = "SKILL005"  # Assuming SKILL005 was created in test_create_skillset

    # Send DELETE request to delete the skill
    response = client.delete(f"/skillsets/{skill_id}")

    # Assert successful deletion
    assert response.status_code == 200
    assert response.json() == {"message": "Skill deleted successfully"}
