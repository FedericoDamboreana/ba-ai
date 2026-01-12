from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from datetime import date
from app.database import get_db
from app.services import item_service, project_service, question_service
from app.services.ai_service import ai_service
from app.prompts import question_generation
from app.models.enums import DocumentationItemStatus, DocumentationType, QuestionType

router = APIRouter(prefix="/api", tags=["documentation_items"])


# Pydantic schemas
class ItemCreate(BaseModel):
    type: DocumentationType
    title: str
    description: str
    deadline: Optional[date] = None


class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[date] = None
    status: Optional[DocumentationItemStatus] = None


class ItemResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    project_id: int
    type: DocumentationType
    title: str
    description: str
    status: DocumentationItemStatus
    deadline: Optional[date]
    generated_content: Optional[dict]
    created_at: str
    updated_at: str


@router.get("/projects/{project_id}/items", response_model=List[ItemResponse])
def list_items(
    project_id: int,
    db: Session = Depends(get_db)
):
    """List all documentation items for a project."""
    items = item_service.get_items_by_project(db, project_id)
    return [
        ItemResponse(
            id=item.id,
            project_id=item.project_id,
            type=item.type,
            title=item.title,
            description=item.description,
            status=item.status,
            deadline=item.deadline,
            generated_content=item.generated_content,
            created_at=item.created_at.isoformat(),
            updated_at=item.updated_at.isoformat()
        )
        for item in items
    ]


@router.post("/projects/{project_id}/items", response_model=ItemResponse, status_code=201)
def create_item(
    project_id: int,
    item: ItemCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new documentation item for a project and generate questions using AI.
    """
    # Get the project
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Create the item
    new_item = item_service.create_item(
        db,
        project_id=project_id,
        doc_type=item.type,
        title=item.title,
        description=item.description,
        deadline=item.deadline
    )

    # Generate questions using AI
    try:
        system_prompt = question_generation.get_system_prompt()
        user_prompt = question_generation.get_user_prompt(project, new_item)
        response_schema = question_generation.get_response_schema()

        ai_response = ai_service.generate_structured_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_schema,
            temperature=0.7
        )

        # Create questions from AI response
        questions_data = []
        for idx, q_data in enumerate(ai_response["questions"]):
            question_data = {
                "doc_item_id": new_item.id,
                "question_text": q_data["question_text"],
                "question_type": QuestionType[q_data["question_type"].upper()],
                "display_order": idx + 1,
                "options": q_data.get("options"),
                "is_critical": q_data["is_critical"],
                "is_answered": False
            }

            # Handle conditional questions
            if q_data.get("parent_question_index") is not None:
                # Parent question index is 0-based in AI response
                parent_idx = q_data["parent_question_index"]
                if parent_idx < len(questions_data):
                    # Store trigger condition
                    question_data["trigger_condition"] = {
                        "parent_question_index": parent_idx,
                        "required_answer": q_data.get("required_answer")
                    }

            questions_data.append(question_data)

        # Create all questions in database
        question_service.create_questions_batch(db, questions_data)

        # Update item status to IN_PROGRESS
        item_service.update_status(db, new_item.id, DocumentationItemStatus.IN_PROGRESS)

    except Exception as e:
        # If AI fails, still return the item but log the error
        print(f"Failed to generate questions: {str(e)}")
        # Item stays in DRAFT status

    # Refresh to get latest state
    db.refresh(new_item)

    return ItemResponse(
        id=new_item.id,
        project_id=new_item.project_id,
        type=new_item.type,
        title=new_item.title,
        description=new_item.description,
        status=new_item.status,
        deadline=new_item.deadline,
        generated_content=new_item.generated_content,
        created_at=new_item.created_at.isoformat(),
        updated_at=new_item.updated_at.isoformat()
    )


@router.get("/items/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific documentation item by ID."""
    item = item_service.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Documentation item not found")

    return ItemResponse(
        id=item.id,
        project_id=item.project_id,
        type=item.type,
        title=item.title,
        description=item.description,
        status=item.status,
        deadline=item.deadline,
        generated_content=item.generated_content,
        created_at=item.created_at.isoformat(),
        updated_at=item.updated_at.isoformat()
    )


@router.put("/items/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item_update: ItemUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing documentation item."""
    updated = item_service.update_item(
        db,
        item_id,
        title=item_update.title,
        description=item_update.description,
        deadline=item_update.deadline,
        status=item_update.status
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Documentation item not found")

    return ItemResponse(
        id=updated.id,
        project_id=updated.project_id,
        type=updated.type,
        title=updated.title,
        description=updated.description,
        status=updated.status,
        deadline=updated.deadline,
        generated_content=updated.generated_content,
        created_at=updated.created_at.isoformat(),
        updated_at=updated.updated_at.isoformat()
    )


@router.delete("/items/{item_id}", status_code=204)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Delete a documentation item."""
    success = item_service.delete_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Documentation item not found")
