from sqlalchemy.orm import Session
from app.models.documentation_item import DocumentationItem
from app.models.enums import DocumentationItemStatus, DocumentationType
from typing import List, Optional
from datetime import datetime, date, timezone


def get_items_by_project(db: Session, project_id: int) -> List[DocumentationItem]:
    """Get all documentation items for a project."""
    return db.query(DocumentationItem)\
        .filter(DocumentationItem.project_id == project_id)\
        .order_by(DocumentationItem.created_at.desc())\
        .all()


def get_item(db: Session, item_id: int) -> Optional[DocumentationItem]:
    """Get a single documentation item by ID."""
    return db.query(DocumentationItem).filter(DocumentationItem.id == item_id).first()


def create_item(
    db: Session,
    project_id: int,
    doc_type: DocumentationType,
    title: str,
    description: str,
    deadline: Optional[date] = None
) -> DocumentationItem:
    """Create a new documentation item."""
    item = DocumentationItem(
        project_id=project_id,
        type=doc_type,
        title=title,
        description=description,
        status=DocumentationItemStatus.DRAFT,
        deadline=deadline
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(
    db: Session,
    item_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    deadline: Optional[date] = None,
    status: Optional[DocumentationItemStatus] = None
) -> Optional[DocumentationItem]:
    """Update an existing documentation item."""
    item = get_item(db, item_id)
    if not item:
        return None

    if title is not None:
        item.title = title
    if description is not None:
        item.description = description
    if deadline is not None:
        item.deadline = deadline
    if status is not None:
        item.status = status

    item.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item_id: int) -> bool:
    """Delete a documentation item."""
    item = get_item(db, item_id)
    if not item:
        return False

    db.delete(item)
    db.commit()
    return True


def update_status(db: Session, item_id: int, status: DocumentationItemStatus) -> Optional[DocumentationItem]:
    """Update the status of a documentation item."""
    item = get_item(db, item_id)
    if not item:
        return None

    item.status = status
    item.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(item)
    return item


def update_generated_content(db: Session, item_id: int, content: dict) -> Optional[DocumentationItem]:
    """Update the generated content of a documentation item."""
    item = get_item(db, item_id)
    if not item:
        return None

    item.generated_content = content
    item.status = DocumentationItemStatus.GENERATED
    item.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(item)
    return item
