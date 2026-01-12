from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from app.database import get_db
from app.services import project_service
from app.models.enums import ProjectStatus

router = APIRouter(prefix="/api/projects", tags=["projects"])


# Pydantic schemas
class ProjectCreate(BaseModel):
    name: str
    description: str
    client: Optional[str] = None
    status: Optional[ProjectStatus] = ProjectStatus.ACTIVE


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    client: Optional[str] = None
    status: Optional[ProjectStatus] = None


class ProjectResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    description: str
    client: Optional[str]
    status: ProjectStatus
    knowledge_base: str
    created_at: str
    updated_at: str


@router.get("", response_model=List[ProjectResponse])
def list_projects(
    status: Optional[ProjectStatus] = Query(None),
    db: Session = Depends(get_db)
):
    """List all projects, optionally filtered by status."""
    projects = project_service.get_projects(db, status=status)
    return [
        ProjectResponse(
            id=p.id,
            name=p.name,
            description=p.description,
            client=p.client,
            status=p.status,
            knowledge_base=p.knowledge_base,
            created_at=p.created_at.isoformat(),
            updated_at=p.updated_at.isoformat()
        )
        for p in projects
    ]


@router.post("", response_model=ProjectResponse, status_code=201)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    """Create a new project."""
    new_project = project_service.create_project(
        db,
        name=project.name,
        description=project.description,
        client=project.client,
        status=project.status
    )
    return ProjectResponse(
        id=new_project.id,
        name=new_project.name,
        description=new_project.description,
        client=new_project.client,
        status=new_project.status,
        knowledge_base=new_project.knowledge_base,
        created_at=new_project.created_at.isoformat(),
        updated_at=new_project.updated_at.isoformat()
    )


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific project by ID."""
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        client=project.client,
        status=project.status,
        knowledge_base=project.knowledge_base,
        created_at=project.created_at.isoformat(),
        updated_at=project.updated_at.isoformat()
    )


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing project."""
    updated = project_service.update_project(
        db,
        project_id,
        name=project_update.name,
        description=project_update.description,
        client=project_update.client,
        status=project_update.status
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found")

    return ProjectResponse(
        id=updated.id,
        name=updated.name,
        description=updated.description,
        client=updated.client,
        status=updated.status,
        knowledge_base=updated.knowledge_base,
        created_at=updated.created_at.isoformat(),
        updated_at=updated.updated_at.isoformat()
    )


@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Delete a project."""
    success = project_service.delete_project(db, project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")


@router.patch("/{project_id}/archive", response_model=ProjectResponse)
def toggle_archive(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Toggle the archive status of a project."""
    project = project_service.toggle_archive(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        client=project.client,
        status=project.status,
        knowledge_base=project.knowledge_base,
        created_at=project.created_at.isoformat(),
        updated_at=project.updated_at.isoformat()
    )
