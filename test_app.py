import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# ── Health check test ──────────────────────────────────
def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'

# ── Create task tests ──────────────────────────────────
def test_create_task(client):
    response = client.post('/tasks',
        data=json.dumps({
            "title": "Test task",
            "description": "Test description",
            "status": "pending"
        }),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test task'
    assert data['status'] == 'pending'
    assert 'id' in data

def test_create_task_no_title(client):
    response = client.post('/tasks',
        data=json.dumps({"description": "No title"}),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_create_task_invalid_status(client):
    response = client.post('/tasks',
        data=json.dumps({
            "title": "Bad status task",
            "status": "invalid_status"
        }),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert 'error' in response.get_json()

# ── Get tasks tests ────────────────────────────────────
def test_get_all_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_single_task(client):
    # First create a task
    create = client.post('/tasks',
        data=json.dumps({"title": "Single task test"}),
        content_type='application/json'
    )
    task_id = create.get_json()['id']

    # Then fetch it
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200
    assert response.get_json()['id'] == task_id

def test_get_nonexistent_task(client):
    response = client.get('/tasks/999999')
    assert response.status_code == 404
    assert 'error' in response.get_json()

# ── Update task tests ──────────────────────────────────
def test_update_task(client):
    # Create first
    create = client.post('/tasks',
        data=json.dumps({"title": "Update me"}),
        content_type='application/json'
    )
    task_id = create.get_json()['id']

    # Update it
    response = client.put(f'/tasks/{task_id}',
        data=json.dumps({"status": "completed"}),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.get_json()['status'] == 'completed'

def test_update_nonexistent_task(client):
    response = client.put('/tasks/999999',
        data=json.dumps({"status": "completed"}),
        content_type='application/json'
    )
    assert response.status_code == 404

# ── Delete task tests ──────────────────────────────────
def test_delete_task(client):
    # Create first
    create = client.post('/tasks',
        data=json.dumps({"title": "Delete me"}),
        content_type='application/json'
    )
    task_id = create.get_json()['id']

    # Delete it
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    assert 'message' in response.get_json()

def test_delete_nonexistent_task(client):
    response = client.delete('/tasks/999999')
    assert response.status_code == 404