import pytest
from flask import Flask, jsonify
from core.server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_ready_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'status' in response.json
    assert response.json['status'] == 'ready'

def test_error_handler_fyle_error(client):
    response = client.get('/nonexistentroute')
    assert response.status_code == 404
    assert 'error' in response.json
    assert response.json['error'] == 'NotFound'

# def test_error_handler_validation_error(client):
#     response = client.post('/student/assignments', json={})
#     assert response.status_code == 400
#     assert 'error' in response.json
#     assert response.json['error'] == 'ValidationError'

# def test_error_handler_integrity_error(client):
#     response = client.post('/student/assignments', json={'content': None})
#     assert response.status_code == 400
#     assert 'error' in response.json
#     assert response.json['error'] == 'IntegrityError'

def test_error_handler_http_exception(client):
    response = client.get('/nonexistentroute')
    assert response.status_code == 404
    assert 'error' in response.json
    assert response.json['error'] == 'NotFound'

def test_blueprint_registration_student(client):
    assert 'student_assignments_resources' in app.blueprints

def test_blueprint_registration_teacher(client):
    assert 'teacher_assignments_resources' in app.blueprints

def test_blueprint_registration_principal(client):
    assert 'principal_assignments_resources' in app.blueprints

