from sqlalchemy.orm import Session
from app.models.question import Question
from app.models.enums import QuestionType
from typing import List, Optional


def get_questions_by_item(db: Session, item_id: int) -> List[Question]:
    """Get all questions for a documentation item."""
    return db.query(Question)\
        .filter(Question.doc_item_id == item_id)\
        .order_by(Question.display_order)\
        .all()


def get_question(db: Session, question_id: int) -> Optional[Question]:
    """Get a single question by ID."""
    return db.query(Question).filter(Question.id == question_id).first()


def create_question(
    db: Session,
    doc_item_id: int,
    question_text: str,
    question_type: QuestionType,
    display_order: int,
    parent_question_id: Optional[int] = None,
    options: Optional[list] = None,
    is_critical: bool = True,
    trigger_condition: Optional[dict] = None
) -> Question:
    """Create a new question."""
    question = Question(
        doc_item_id=doc_item_id,
        parent_question_id=parent_question_id,
        question_text=question_text,
        question_type=question_type,
        options=options,
        is_critical=is_critical,
        display_order=display_order,
        trigger_condition=trigger_condition,
        is_answered=False
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def create_questions_batch(db: Session, questions_data: List[dict]) -> List[Question]:
    """Create multiple questions at once."""
    questions = []
    for data in questions_data:
        question = Question(**data)
        questions.append(question)
        db.add(question)

    db.commit()
    for question in questions:
        db.refresh(question)

    return questions


def update_answer(db: Session, question_id: int, answer: str) -> Optional[Question]:
    """Update the answer for a question."""
    question = get_question(db, question_id)
    if not question:
        return None

    question.answer = answer
    question.is_answered = True
    db.commit()
    db.refresh(question)
    return question


def clear_answer(db: Session, question_id: int) -> Optional[Question]:
    """Clear the answer for a question."""
    question = get_question(db, question_id)
    if not question:
        return None

    question.answer = None
    question.is_answered = False
    db.commit()
    db.refresh(question)
    return question


def get_completion_status(db: Session, item_id: int) -> dict:
    """Get the completion status for all questions in a documentation item."""
    questions = get_questions_by_item(db, item_id)

    total = len(questions)
    answered = sum(1 for q in questions if q.is_answered)
    critical = sum(1 for q in questions if q.is_critical)
    critical_answered = sum(1 for q in questions if q.is_critical and q.is_answered)

    return {
        "total_questions": total,
        "answered_questions": answered,
        "critical_questions": critical,
        "critical_answered": critical_answered,
        "all_critical_answered": critical == critical_answered,
        "all_answered": total == answered
    }


def delete_questions_by_item(db: Session, item_id: int) -> int:
    """Delete all questions for a documentation item. Returns count of deleted questions."""
    count = db.query(Question).filter(Question.doc_item_id == item_id).delete()
    db.commit()
    return count
