from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base
from app.models.enums import ProjectStatus

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    client = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.ACTIVE, nullable=False)
    knowledge_base = Column(Text, nullable=True, default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    documentation_items = relationship("DocumentationItem", back_populates="project", cascade="all, delete-orphan")
