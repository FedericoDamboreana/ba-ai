from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base
from app.models.enums import DocumentationItemStatus, DocumentationType

class DocumentationItem(Base):
    __tablename__ = "documentation_items"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    type = Column(Enum(DocumentationType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(DocumentationItemStatus), default=DocumentationItemStatus.DRAFT, nullable=False)
    deadline = Column(Date, nullable=True)
    generated_content = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    project = relationship("Project", back_populates="documentation_items")
    questions = relationship("Question", back_populates="documentation_item", cascade="all, delete-orphan")
