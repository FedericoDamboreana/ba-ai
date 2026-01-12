from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.enums import ProjectStatus
from typing import List, Optional
from datetime import datetime, timezone


def get_projects(db: Session, status: Optional[ProjectStatus] = None) -> List[Project]:
    """Get all projects, optionally filtered by status."""
    query = db.query(Project)
    if status:
        query = query.filter(Project.status == status)
    return query.order_by(Project.updated_at.desc()).all()


def get_project(db: Session, project_id: int) -> Optional[Project]:
    """Get a single project by ID."""
    return db.query(Project).filter(Project.id == project_id).first()


def create_project(
    db: Session,
    name: str,
    description: str,
    client: Optional[str] = None,
    status: ProjectStatus = ProjectStatus.ACTIVE
) -> Project:
    """Create a new project."""
    project = Project(
        name=name,
        description=description,
        client=client,
        status=status,
        knowledge_base=""
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def update_project(
    db: Session,
    project_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    client: Optional[str] = None,
    status: Optional[ProjectStatus] = None
) -> Optional[Project]:
    """Update an existing project."""
    project = get_project(db, project_id)
    if not project:
        return None

    if name is not None:
        project.name = name
    if description is not None:
        project.description = description
    if client is not None:
        project.client = client
    if status is not None:
        project.status = status

    project.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project_id: int) -> bool:
    """Delete a project."""
    project = get_project(db, project_id)
    if not project:
        return False

    db.delete(project)
    db.commit()
    return True


def toggle_archive(db: Session, project_id: int) -> Optional[Project]:
    """Toggle project archive status."""
    project = get_project(db, project_id)
    if not project:
        return None

    if project.status == ProjectStatus.ARCHIVED:
        project.status = ProjectStatus.ACTIVE
    else:
        project.status = ProjectStatus.ARCHIVED

    project.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(project)
    return project


def update_knowledge_base(db: Session, project_id: int, knowledge_base: str) -> Optional[Project]:
    """Update project knowledge base."""
    project = get_project(db, project_id)
    if not project:
        return None

    project.knowledge_base = knowledge_base
    project.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(project)
    return project
