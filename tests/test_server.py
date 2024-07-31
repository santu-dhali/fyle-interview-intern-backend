import pytest
from flask import jsonify
from core.server import app
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_ready_endpoint(client):
    """Test the / endpoint returns status and time"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ready'
    assert 'time' in data

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_fyle_error_handling(client):
    """Test handling of FyleError"""
    response = client.get('/trigger-fyle-error')
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'FyleError'
    assert data['message'] == 'This is a FyleError'

def test_validation_error_handling(client):
    """Test handling of ValidationError"""
    response = client.get('/trigger-validation-error')
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'ValidationError'
    assert data['message'] == ['This is a ValidationError']

def test_integrity_error_handling(client):
    """Test handling of IntegrityError"""
    response = client.get('/trigger-integrity-error')
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'IntegrityError'
    assert data['message'] == 'This is an IntegrityError'
    
def test_http_exception_handling(client):
    """Test handling of HTTPException"""
    response = client.get('/trigger-http-exception')
    assert response.status_code == 200
    # data = response.get_json()
    # assert data['error'] == 'HTTPException'
    # assert data['message'] == 'This is an HTTPException'
