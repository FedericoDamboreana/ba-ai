from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.enums import QuestionType

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    doc_item_id = Column(Integer, ForeignKey("documentation_items.id"), nullable=False)
    parent_question_id = Column(Integer, ForeignKey("questions.id"), nullable=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(Enum(QuestionType), nullable=False)
    options = Column(JSON, nullable=True)
    is_critical = Column(Boolean, default=True, nullable=False)
    display_order = Column(Integer, nullable=False)
    answer = Column(Text, nullable=True)
    is_answered = Column(Boolean, default=False, nullable=False)
    trigger_condition = Column(JSON, nullable=True)

    documentation_item = relationship("DocumentationItem", back_populates="questions")
    parent_question = relationship("Question", remote_side=[id], backref="child_questions")
