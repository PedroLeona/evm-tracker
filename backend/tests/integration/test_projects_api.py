from tests.integration.helpers import PROJECT_KEYS, create_project

MISSING_ID = 999


def test_health_endpoint_reports_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_project_returns_201_with_the_project_contract(client):
    response = client.post("/api/projects", json={"name": "ERP migration", "description": "Demo"})

    assert response.status_code == 201
    body = response.json()
    assert set(body) == PROJECT_KEYS
    assert body["name"] == "ERP migration"
    assert isinstance(body["id"], int)


def test_create_project_without_name_returns_422(client):
    response = client.post("/api/projects", json={"description": "no name"})

    assert response.status_code == 422


def test_create_project_with_empty_name_returns_422(client):
    response = client.post("/api/projects", json={"name": ""})

    assert response.status_code == 422


def test_list_projects_returns_every_created_project(client):
    create_project(client, "First")
    create_project(client, "Second")

    response = client.get("/api/projects")

    assert response.status_code == 200
    assert [project["name"] for project in response.json()] == ["First", "Second"]


def test_get_project_returns_the_project(client):
    project = create_project(client)

    response = client.get(f"/api/projects/{project['id']}")

    assert response.status_code == 200
    assert response.json() == project


def test_get_unknown_project_returns_404_with_error_contract(client):
    response = client.get(f"/api/projects/{MISSING_ID}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Project {MISSING_ID} not found"}


def test_update_project_replaces_its_data(client):
    project = create_project(client)

    response = client.put(
        f"/api/projects/{project['id']}", json={"name": "Renamed", "description": None}
    )

    assert response.status_code == 200
    assert response.json() == {"id": project["id"], "name": "Renamed", "description": None}


def test_update_unknown_project_returns_404(client):
    response = client.put(f"/api/projects/{MISSING_ID}", json={"name": "x"})

    assert response.status_code == 404


def test_delete_project_returns_204_and_removes_it(client):
    project = create_project(client)

    delete_response = client.delete(f"/api/projects/{project['id']}")
    get_response = client.get(f"/api/projects/{project['id']}")

    assert delete_response.status_code == 204
    assert delete_response.content == b""
    assert get_response.status_code == 404


def test_delete_unknown_project_returns_404(client):
    response = client.delete(f"/api/projects/{MISSING_ID}")

    assert response.status_code == 404


def test_swagger_ui_is_served_at_api_docs(client):
    response = client.get("/api-docs")

    assert response.status_code == 200
    assert "swagger" in response.text.lower()


def test_openapi_document_describes_every_endpoint_with_error_codes(client):
    document = client.get("/openapi.json").json()

    paths = document["paths"]
    assert "/api/projects/{project_id}/evm" in paths
    assert "/api/activities/{activity_id}" in paths
    assert "404" in paths["/api/projects/{project_id}"]["get"]["responses"]
    assert "422" in paths["/api/projects/{project_id}/activities"]["post"]["responses"]
