from app.models.enums import ProjectStatus


def test_create_project(client):
    """Test creating a new project."""
    response = client.post(
        "/api/projects",
        json={
            "name": "Test Project",
            "description": "Test description",
            "client": "Test Client"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["description"] == "Test description"
    assert data["client"] == "Test Client"
    assert data["status"] == "Active"
    assert "id" in data


def test_list_projects(client):
    """Test listing all projects."""
    # Create two projects
    client.post(
        "/api/projects",
        json={"name": "Project 1", "description": "Desc 1"}
    )
    client.post(
        "/api/projects",
        json={"name": "Project 2", "description": "Desc 2"}
    )

    # List all projects
    response = client.get("/api/projects")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_list_projects_by_status(client):
    """Test filtering projects by status."""
    # Create active and archived projects
    client.post(
        "/api/projects",
        json={"name": "Active Project", "description": "Desc", "status": "Active"}
    )
    archived_response = client.post(
        "/api/projects",
        json={"name": "Archived Project", "description": "Desc", "status": "Archived"}
    )

    # List only active projects
    response = client.get("/api/projects?status=Active")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Active Project"

    # List only archived projects
    response = client.get("/api/projects?status=Archived")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Archived Project"


def test_get_project(client):
    """Test getting a specific project."""
    # Create a project
    create_response = client.post(
        "/api/projects",
        json={"name": "Test Project", "description": "Test desc"}
    )
    project_id = create_response.json()["id"]

    # Get the project
    response = client.get(f"/api/projects/{project_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project_id
    assert data["name"] == "Test Project"


def test_get_nonexistent_project(client):
    """Test getting a project that doesn't exist."""
    response = client.get("/api/projects/99999")
    assert response.status_code == 404


def test_update_project(client):
    """Test updating a project."""
    # Create a project
    create_response = client.post(
        "/api/projects",
        json={"name": "Original Name", "description": "Original desc"}
    )
    project_id = create_response.json()["id"]

    # Update the project
    response = client.put(
        f"/api/projects/{project_id}",
        json={"name": "Updated Name", "description": "Updated desc"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["description"] == "Updated desc"


def test_delete_project(client):
    """Test deleting a project."""
    # Create a project
    create_response = client.post(
        "/api/projects",
        json={"name": "To Delete", "description": "Will be deleted"}
    )
    project_id = create_response.json()["id"]

    # Delete the project
    response = client.delete(f"/api/projects/{project_id}")
    assert response.status_code == 204

    # Verify it's deleted
    response = client.get(f"/api/projects/{project_id}")
    assert response.status_code == 404


def test_toggle_archive(client):
    """Test toggling archive status."""
    # Create an active project
    create_response = client.post(
        "/api/projects",
        json={"name": "Test Project", "description": "Test desc"}
    )
    project_id = create_response.json()["id"]

    # Archive it
    response = client.patch(f"/api/projects/{project_id}/archive")
    assert response.status_code == 200
    assert response.json()["status"] == "Archived"

    # Unarchive it
    response = client.patch(f"/api/projects/{project_id}/archive")
    assert response.status_code == 200
    assert response.json()["status"] == "Active"
