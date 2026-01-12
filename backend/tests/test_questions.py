from app.models.enums import QuestionType
from app.services import question_service
from unittest.mock import patch


# Mock AI response
MOCK_AI_QUESTIONS = {
    "questions": [
        {"question_text": "Test question?", "question_type": "Text", "is_critical": True}
    ]
}


@patch('app.services.ai_service.ai_service.generate_structured_response')
def test_list_questions(mock_ai, client, db_session):
    """Test listing questions for an item."""
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

    # Create questions directly via service
    question_service.create_question(
        db_session,
        doc_item_id=item_id,
        question_text="Who are the users?",
        question_type=QuestionType.TEXT,
        display_order=1
    )
    question_service.create_question(
        db_session,
        doc_item_id=item_id,
        question_text="What is the priority?",
        question_type=QuestionType.MULTIPLE_CHOICE,
        display_order=2,
        options=["High", "Medium", "Low"]
    )

    # List questions
    response = client.get(f"/api/items/{item_id}/questions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["question_text"] == "Who are the users?"
    assert data[1]["question_type"] == "MultipleChoice"


@patch('app.services.ai_service.ai_service.generate_structured_response')
def test_update_answer(mock_ai, client, db_session):
    """Test updating an answer to a question."""
    # Create project, item, and question
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

    question = question_service.create_question(
        db_session,
        doc_item_id=item_id,
        question_text="Test question?",
        question_type=QuestionType.TEXT,
        display_order=1
    )

    # Update the answer
    response = client.put(
        f"/api/questions/{question.id}",
        json={"answer": "This is my answer"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "This is my answer"
    assert data["is_answered"] is True


@patch('app.services.ai_service.ai_service.generate_structured_response')
def test_validate_completeness(mock_ai, client, db_session):
    """Test validating if all critical questions are answered."""
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

    # Create critical and non-critical questions
    q1 = question_service.create_question(
        db_session,
        doc_item_id=item_id,
        question_text="Critical question?",
        question_type=QuestionType.TEXT,
        display_order=1,
        is_critical=True
    )
    q2 = question_service.create_question(
        db_session,
        doc_item_id=item_id,
        question_text="Optional question?",
        question_type=QuestionType.TEXT,
        display_order=2,
        is_critical=False
    )

    # Check status before answering
    response = client.post(f"/api/items/{item_id}/validate")
    assert response.status_code == 200
    data = response.json()
    assert data["all_critical_answered"] is False
    assert data["total_questions"] == 2
    assert data["critical_questions"] == 1

    # Answer the critical question
    question_service.update_answer(db_session, q1.id, "Answer to critical")

    # Check status after answering critical
    response = client.post(f"/api/items/{item_id}/validate")
    assert response.status_code == 200
    data = response.json()
    assert data["all_critical_answered"] is True
    assert data["answered_questions"] == 1


@patch('app.services.ai_service.ai_service.generate_structured_response')
def test_question_with_options(mock_ai, client, db_session):
    """Test creating and retrieving questions with multiple choice options."""
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

    # Create question with options
    question = question_service.create_question(
        db_session,
        doc_item_id=item_id,
        question_text="Select priority",
        question_type=QuestionType.MULTIPLE_CHOICE,
        display_order=1,
        options=["High", "Medium", "Low"]
    )

    # Get the questions
    response = client.get(f"/api/items/{item_id}/questions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["options"] == ["High", "Medium", "Low"]
