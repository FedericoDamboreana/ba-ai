from unittest.mock import patch


# Mock AI responses
MOCK_AI_QUESTIONS = {
    "questions": [
        {"question_text": "Test question 1?", "question_type": "Text", "is_critical": True},
        {"question_text": "Test question 2?", "question_type": "Text", "is_critical": True}
    ]
}

MOCK_AI_DOC = {
    "title": "Generated User Story",
    "user_story": {
        "as_a": "user",
        "i_want": "to login",
        "so_that": "I can access my account"
    },
    "acceptance_criteria": [
        {
            "scenario_name": "Successful login",
            "given": ["User is on login page"],
            "when": ["User enters valid credentials"],
            "then": ["User is logged in"]
        }
    ]
}

MOCK_KB = {"knowledge_base": "Updated knowledge base with new information"}


@patch('app.services.ai_service.ai_service.generate_structured_response')
def test_generate_documentation(mock_ai, client):
    """Test generating documentation with AI."""
    # Mock will be called 3 times: 1) questions, 2) doc generation, 3) knowledge base
    mock_ai.side_effect = [MOCK_AI_QUESTIONS, MOCK_AI_DOC, MOCK_KB]

    # Create project and item
    project_response = client.post(
        "/api/projects",
        json={"name": "Test Project", "description": "Test desc"}
    )
    project_id = project_response.json()["id"]

    item_response = client.post(
        f"/api/projects/{project_id}/items",
        json={"type": "UserStory", "title": "Test Item", "description": "Test desc"}
    )
    item_id = item_response.json()["id"]

    # Answer all critical questions
    questions_response = client.get(f"/api/items/{item_id}/questions")
    questions = questions_response.json()

    for question in questions:
        if question["is_critical"]:
            client.put(
                f"/api/questions/{question['id']}",
                json={"answer": "Test answer"}
            )

    # Generate documentation
    response = client.post(f"/api/items/{item_id}/generate", json={})
    assert response.status_code == 200
    data = response.json()
    assert data["item_id"] == item_id
    assert "content" in data
    assert data["content"]["title"] == "Generated User Story"
    assert "message" in data


@patch('app.services.ai_service.ai_service.generate_structured_response')
def test_regenerate_documentation(mock_ai, client):
    """Test regenerating documentation with feedback."""
    # Mock: 1) questions, 2) doc gen, 3) KB update, 4) regenerate
    mock_ai.side_effect = [MOCK_AI_QUESTIONS, MOCK_AI_DOC, MOCK_KB, MOCK_AI_DOC]

    # Create project and item
    project_response = client.post(
        "/api/projects",
        json={"name": "Test Project", "description": "Test desc"}
    )
    project_id = project_response.json()["id"]

    item_response = client.post(
        f"/api/projects/{project_id}/items",
        json={"type": "PRD", "title": "Test PRD", "description": "Test desc"}
    )
    item_id = item_response.json()["id"]

    # Answer questions
    questions_response = client.get(f"/api/items/{item_id}/questions")
    for question in questions_response.json():
        if question["is_critical"]:
            client.put(
                f"/api/questions/{question['id']}",
                json={"answer": "Test answer"}
            )

    # Initial generation
    client.post(f"/api/items/{item_id}/generate", json={})

    # Regenerate with feedback
    response = client.post(
        f"/api/items/{item_id}/regenerate",
        json={"feedback": "Make it more detailed"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["item_id"] == item_id
    assert "content" in data


@patch('app.services.ai_service.ai_service.generate_structured_response')
def test_export_documentation(mock_ai, client):
    """Test exporting documentation (placeholder endpoint)."""
    # Mock: 1) questions, 2) doc gen, 3) KB update
    mock_ai.side_effect = [MOCK_AI_QUESTIONS, MOCK_AI_DOC, MOCK_KB]

    # Create project and item
    project_response = client.post(
        "/api/projects",
        json={"name": "Test Project", "description": "Test desc"}
    )
    project_id = project_response.json()["id"]

    item_response = client.post(
        f"/api/projects/{project_id}/items",
        json={"type": "Epic", "title": "Test Epic", "description": "Test desc"}
    )
    item_id = item_response.json()["id"]

    # Answer questions
    questions_response = client.get(f"/api/items/{item_id}/questions")
    for question in questions_response.json():
        if question["is_critical"]:
            client.put(
                f"/api/questions/{question['id']}",
                json={"answer": "Test answer"}
            )

    # Generate first to have content
    client.post(f"/api/items/{item_id}/generate", json={})

    # Export
    response = client.get(f"/api/items/{item_id}/export")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["item_id"] == item_id


@patch('app.services.ai_service.ai_service.generate_structured_response')
def test_export_without_content(mock_ai, client):
    """Test exporting documentation without generated content."""
    mock_ai.return_value = MOCK_AI_QUESTIONS

    # Create project and item
    project_response = client.post(
        "/api/projects",
        json={"name": "Test Project", "description": "Test desc"}
    )
    project_id = project_response.json()["id"]

    item_response = client.post(
        f"/api/projects/{project_id}/items",
        json={"type": "FRS", "title": "Test FRS", "description": "Test desc"}
    )
    item_id = item_response.json()["id"]

    # Try to export without generating first
    response = client.get(f"/api/items/{item_id}/export")
    assert response.status_code == 400
    assert "No generated content" in response.json()["detail"]


def test_generate_nonexistent_item(client):
    """Test generating documentation for non-existent item."""
    response = client.post("/api/items/99999/generate", json={})
    assert response.status_code == 404


@patch('app.services.ai_service.ai_service.generate_structured_response')
def test_generate_without_questions_answered(mock_ai, client):
    """Test that generation fails when questions aren't answered."""
    mock_ai.return_value = MOCK_AI_QUESTIONS

    # Create project and item
    project_response = client.post(
        "/api/projects",
        json={"name": "Test Project", "description": "Test desc"}
    )
    project_id = project_response.json()["id"]

    item_response = client.post(
        f"/api/projects/{project_id}/items",
        json={"type": "UserStory", "title": "Test Item", "description": "Test desc"}
    )
    item_id = item_response.json()["id"]

    # Try to generate without answering questions
    response = client.post(f"/api/items/{item_id}/generate", json={})
    assert response.status_code == 400
    assert "Not all critical questions answered" in response.json()["detail"]
