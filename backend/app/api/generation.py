from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from app.services import item_service, project_service, question_service
from app.services.ai_service import ai_service
from app.prompts import doc_generation, knowledge_base

router = APIRouter(prefix="/api/items", tags=["generation"])


# Pydantic schemas
class GenerateRequest(BaseModel):
    """Request to generate documentation."""
    pass


class RegenerateRequest(BaseModel):
    """Request to regenerate documentation with feedback."""
    feedback: str


class GenerateResponse(BaseModel):
    """Response containing generated documentation."""
    item_id: int
    content: dict
    message: str


@router.post("/{item_id}/generate", response_model=GenerateResponse)
def generate_documentation(
    item_id: int,
    request: GenerateRequest,
    db: Session = Depends(get_db)
):
    """
    Generate documentation for a documentation item using AI.
    """
    # Get the item
    item = item_service.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Documentation item not found")

    # Get the project
    project = project_service.get_project(db, item.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get all questions
    questions = question_service.get_questions_by_item(db, item_id)
    if not questions:
        raise HTTPException(status_code=400, detail="No questions found for this item")

    # Check if all critical questions are answered
    status = question_service.get_completion_status(db, item_id)
    if not status["all_critical_answered"]:
        raise HTTPException(
            status_code=400,
            detail=f"Not all critical questions answered ({status['critical_answered']}/{status['critical_questions']})"
        )

    try:
        # Generate documentation using AI
        system_prompt = doc_generation.get_system_prompt(item.type.value)
        user_prompt = doc_generation.get_user_prompt(project, item, questions)
        response_schema = doc_generation.get_response_schema(item.type.value)

        generated_content = ai_service.generate_structured_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_schema,
            temperature=0.7
        )

        # Update the item with generated content
        item_service.update_generated_content(db, item_id, generated_content)

        # Update knowledge base
        _update_knowledge_base(db, project, item, questions, generated_content)

        return GenerateResponse(
            item_id=item_id,
            content=generated_content,
            message="Documentation generated successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate documentation: {str(e)}")


@router.post("/{item_id}/regenerate", response_model=GenerateResponse)
def regenerate_documentation(
    item_id: int,
    request: RegenerateRequest,
    db: Session = Depends(get_db)
):
    """
    Regenerate documentation with user feedback.
    """
    # Get the item
    item = item_service.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Documentation item not found")

    if not item.generated_content:
        raise HTTPException(status_code=400, detail="No existing documentation to regenerate")

    # Get the project
    project = project_service.get_project(db, item.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get all questions
    questions = question_service.get_questions_by_item(db, item_id)

    try:
        # Generate documentation with feedback
        system_prompt = doc_generation.get_system_prompt(item.type.value)
        user_prompt = doc_generation.get_user_prompt(
            project, item, questions, feedback=request.feedback
        )
        response_schema = doc_generation.get_response_schema(item.type.value)

        generated_content = ai_service.generate_structured_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_schema,
            temperature=0.7
        )

        # Update the item with regenerated content
        item_service.update_generated_content(db, item_id, generated_content)

        return GenerateResponse(
            item_id=item_id,
            content=generated_content,
            message="Documentation regenerated successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to regenerate documentation: {str(e)}")


@router.get("/{item_id}/export")
def export_documentation(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Export documentation as Word document.

    This is a placeholder endpoint. Full export functionality will be implemented in Phase 5.
    """
    item = item_service.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Documentation item not found")

    if not item.generated_content:
        raise HTTPException(status_code=400, detail="No generated content to export")

    return {
        "message": "Word export will be implemented in Phase 5",
        "item_id": item_id,
        "title": item.title
    }


def _update_knowledge_base(db: Session, project, item, questions, generated_content):
    """
    Update the project knowledge base after generating documentation.

    Args:
        db: Database session
        project: The project
        item: The documentation item
        questions: List of questions
        generated_content: The generated documentation
    """
    try:
        # Prepare Q&A for knowledge base
        qa_list = []
        for q in questions:
            if q.is_answered:
                qa_list.append({
                    "question": q.question_text,
                    "answer": q.answer
                })

        # Generate updated knowledge base using AI
        system_prompt = knowledge_base.get_system_prompt()
        user_prompt = knowledge_base.get_user_prompt(
            project, item, generated_content, qa_list
        )
        response_schema = knowledge_base.get_response_schema()

        kb_response = ai_service.generate_structured_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_schema,
            temperature=0.5
        )

        # Update the project's knowledge base
        new_kb = kb_response["knowledge_base"]
        project_service.update_knowledge_base(db, project.id, new_kb)

    except Exception as e:
        # Knowledge base update is not critical, just log the error
        print(f"Failed to update knowledge base: {str(e)}")
