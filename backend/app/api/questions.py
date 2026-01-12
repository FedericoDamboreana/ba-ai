from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.database import get_db
from app.services import question_service
from app.models.enums import QuestionType

router = APIRouter(prefix="/api", tags=["questions"])


# Pydantic schemas
class AnswerUpdate(BaseModel):
    answer: str


class QuestionResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    doc_item_id: int
    parent_question_id: int | None
    question_text: str
    question_type: QuestionType
    options: list | None
    is_critical: bool
    display_order: int
    answer: str | None
    is_answered: bool
    trigger_condition: dict | None


class CompletionStatusResponse(BaseModel):
    total_questions: int
    answered_questions: int
    critical_questions: int
    critical_answered: int
    all_critical_answered: bool
    all_answered: bool


@router.get("/items/{item_id}/questions", response_model=List[QuestionResponse])
def list_questions(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Get all questions for a documentation item."""
    questions = question_service.get_questions_by_item(db, item_id)
    return [
        QuestionResponse(
            id=q.id,
            doc_item_id=q.doc_item_id,
            parent_question_id=q.parent_question_id,
            question_text=q.question_text,
            question_type=q.question_type,
            options=q.options,
            is_critical=q.is_critical,
            display_order=q.display_order,
            answer=q.answer,
            is_answered=q.is_answered,
            trigger_condition=q.trigger_condition
        )
        for q in questions
    ]


@router.put("/questions/{question_id}", response_model=QuestionResponse)
def update_answer(
    question_id: int,
    answer_update: AnswerUpdate,
    db: Session = Depends(get_db)
):
    """Update the answer for a question."""
    updated = question_service.update_answer(db, question_id, answer_update.answer)
    if not updated:
        raise HTTPException(status_code=404, detail="Question not found")

    return QuestionResponse(
        id=updated.id,
        doc_item_id=updated.doc_item_id,
        parent_question_id=updated.parent_question_id,
        question_text=updated.question_text,
        question_type=updated.question_type,
        options=updated.options,
        is_critical=updated.is_critical,
        display_order=updated.display_order,
        answer=updated.answer,
        is_answered=updated.is_answered,
        trigger_condition=updated.trigger_condition
    )


@router.post("/items/{item_id}/validate", response_model=CompletionStatusResponse)
def validate_completeness(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Check if all critical questions are answered and if ready for generation."""
    status = question_service.get_completion_status(db, item_id)
    return CompletionStatusResponse(**status)
