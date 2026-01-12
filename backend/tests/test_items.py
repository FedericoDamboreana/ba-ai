from datetime import date, timedelta
from unittest.mock import patch


# Mock AI response for question generation
MOCK_AI_QUESTIONS = {
    "questions": [
        {
            "question_text": "Who are the primary users?",
            "question_type": "Text",
            "is_critical": True
        },
        {
            "question_text": "What is the main benefit?",
            "question_type": "Text",
            "is_critical": True
        }
    ]
}


@patch('app.services.ai_service.ai_service.generate_structured_response')
def test_create_item(mock_ai, client):
    """Test creating a documentation item."""
    mock_ai.return_value = MOCK_AI_QUESTIONS

    # First create a project
    project_response = client.post(
        "/api/projects",
        json={"name": "Test Project", "description": "Test desc"}
    )
    project_id = project_response.json()["id"]

    # Create an item
    response = client.post(
        f"/api/projects/{project_id}/items",
        json={
            "type": "UserStory",
            "title": "User Login",
            "description": "Implement user login functionality"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "User Login"
    assert data["type"] == "UserStory"
    assert data["status"] == "InProgress"  # Changed to InProgress after questions generated
    assert data["project_id"] == project_id


@patch('app.services.ai_service.ai_service.generate_structured_response')
def test_list_items_for_project(mock_ai, client):
    """Test listing all items for a project."""
    mock_ai.return_value = MOCK_AI_QUESTIONS

    # Create a project
    project_response = client.post(
        "/api/projects",
        json={"name": "Test Project", "description": "Test desc"}
    )
    project_id = project_response.json()["id"]

    # Create multiple items
    client.post(
        f"/api/projects/{project_id}/items",
        json={"type": "UserStory", "title": "Item 1", "description": "Desc 1"}
    )
    client.post(
        f"/api/projects/{project_id}/items",
        json={"type": "PRD", "title": "Item 2", "description": "Desc 2"}
    )

    # List items
    response = client.get(f"/api/projects/{project_id}/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@patch('app.services.ai_service.ai_service.generate_structured_response')
def test_get_item(mock_ai, client):
    """Test getting a specific item."""
    mock_ai.return_value = MOCK_AI_QUESTIONS

    # Create project and item
    project_response = client.post(
        "/api/projects",
        json={"name": "Test Project", "description": "Test desc"}
    )
    project_id = project_response.json()["id"]

    item_response = client.post(
        f"/api/projects/{project_id}/items",
        json={"type": "Epic", "title": "Test Epic", "description": "Epic desc"}
    )
    item_id = item_response.json()["id"]

    # Get the item
    response = client.get(f"/api/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["title"] == "Test Epic"


@patch('app.services.ai_service.ai_service.generate_structured_response')
def test_update_item(mock_ai, client):
    """Test updating an item."""
    mock_ai.return_value = MOCK_AI_QUESTIONS

    # Create project and item
    project_response = client.post(
        "/api/projects",
        json={"name": "Test Project", "description": "Test desc"}
    )
    project_id = project_response.json()["id"]

    item_response = client.post(
        f"/api/projects/{project_id}/items",
        json={"type": "FRS", "title": "Original", "description": "Original desc"}
    )
    item_id = item_response.json()["id"]

    # Update the item
    response = client.put(
        f"/api/items/{item_id}",
        json={"title": "Updated Title", "status": "InProgress"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == "InProgress"


@patch('app.services.ai_service.ai_service.generate_structured_response')
def test_delete_item(mock_ai, client):
    """Test deleting an item."""
    mock_ai.return_value = MOCK_AI_QUESTIONS

    # Create project and item
    project_response = client.post(
        "/api/projects",
        json={"name": "Test Project", "description": "Test desc"}
    )
    project_id = project_response.json()["id"]

    item_response = client.post(
        f"/api/projects/{project_id}/items",
        json={"type": "UserStory", "title": "To Delete", "description": "Will be deleted"}
    )
    item_id = item_response.json()["id"]

    # Delete the item
    response = client.delete(f"/api/items/{item_id}")
    assert response.status_code == 204

    # Verify it's deleted
    response = client.get(f"/api/items/{item_id}")
    assert response.status_code == 404


@patch('app.services.ai_service.ai_service.generate_structured_response')
def test_create_item_with_deadline(mock_ai, client):
    """Test creating an item with a deadline."""
    mock_ai.return_value = MOCK_AI_QUESTIONS

    # Create a project
    project_response = client.post(
        "/api/projects",
        json={"name": "Test Project", "description": "Test desc"}
    )
    project_id = project_response.json()["id"]

    # Create item with deadline
    deadline = (date.today() + timedelta(days=7)).isoformat()
    response = client.post(
        f"/api/projects/{project_id}/items",
        json={
            "type": "UserStory",
            "title": "Urgent Item",
            "description": "Has deadline",
            "deadline": deadline
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["deadline"] == deadline
