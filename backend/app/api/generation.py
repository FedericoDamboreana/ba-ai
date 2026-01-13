from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from urllib.parse import quote
import re
from app.database import get_db
from app.services import item_service, project_service, question_service
from app.services.ai_service import ai_service
from app.services.export_service import export_to_word
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
            response_format=response_schema
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
            response_format=response_schema
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


def sanitize_filename(name: str) -> str:
    """
    Sanitize a string for use in a filename.
    Removes or replaces characters that are invalid in filenames.
    """
    # Replace characters that are invalid in filenames
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', name)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(' .')
    return sanitized


@router.get("/{item_id}/export")
def export_documentation(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Export documentation as Word document (.docx).
    """
    item = item_service.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Documentation item not found")

    if not item.generated_content:
        raise HTTPException(status_code=400, detail="No generated content to export")

    # Get the project for filename
    project = project_service.get_project(db, item.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        # Prepare item data for export
        item_data = {
            "title": item.title,
            "description": item.description,
            "type": item.type.value
        }

        # Generate Word document
        buffer = export_to_word(item_data, item.generated_content, item.type.value)

        # Read the complete content from the buffer
        content = buffer.getvalue()

        # Create filename: project_name - documentation_name.docx
        project_name = sanitize_filename(project.name)
        item_title = sanitize_filename(item.title)
        filename = f"{project_name} - {item_title}.docx"

        # Create Content-Disposition header with RFC 5987 encoding for non-ASCII characters
        # filename* uses UTF-8 encoding, filename is ASCII fallback
        ascii_filename = filename.encode('ascii', 'replace').decode('ascii')
        encoded_filename = quote(filename, safe='')

        content_disposition = (
            f"attachment; "
            f"filename=\"{ascii_filename}\"; "
            f"filename*=UTF-8''{encoded_filename}"
        )

        # Return as Response with complete content (not streaming)
        return Response(
            content=content,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": content_disposition}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export document: {str(e)}")


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
            response_format=response_schema
        )

        # Update the project's knowledge base
        new_kb = kb_response["knowledge_base"]
        project_service.update_knowledge_base(db, project.id, new_kb)

    except Exception as e:
        # Knowledge base update is not critical, just log the error
        print(f"Failed to update knowledge base: {str(e)}")
