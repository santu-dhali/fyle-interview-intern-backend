# tests/conftest.py

import pytest
import json
from tests import app  # Import the app instance from tests

# Existing fixtures
@pytest.fixture
def client():
    return app.test_client()

@pytest.fixture
def h_student_1():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 1,
            'user_id': 1
        })
    }
    return headers

@pytest.fixture
def h_student_2():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 2,
            'user_id': 2
        })
    }
    return headers

@pytest.fixture
def h_grading_by_teacher_2():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 2,
            'user_id': 4
        })
    }
    return headers

@pytest.fixture
def h_teacher_1():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 1,
            'user_id': 3
        })
    }
    return headers

@pytest.fixture
def h_teacher_2():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 2,
            'user_id': 4
        })
    }
    return headers

@pytest.fixture
def h_principal():
    headers = {
        'X-Principal': json.dumps({
            'principal_id': 1,
            'user_id': 5
        })
    }
    return headers

# New fixture to set up the Flask app context
@pytest.fixture(scope='module')
def app_context():
    with app.app_context():
        yield app

# Update the existing client fixture to use the app fixture
@pytest.fixture
def client(app_context):
    return app.test_client()

# Optional: Add a runner fixture if needed for CLI commands
@pytest.fixture
def runner(app_context):
    return app.test_cli_runner()
