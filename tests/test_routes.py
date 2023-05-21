import pytest
import os
from app import create_app

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'CLIENT_ID': os.getenv('CLIENT_ID'),
        'CLIENT_SECRET': os.getenv('CLIENT_SECRET'),
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to my app!' in response.data

def test_authorize_redirect(client):
    response = client.get('/authorize', follow_redirects=False)
    assert response.status_code == 302

def test_oauth2callback_without_code(client):
    response = client.get('/oauth2callback')
    assert response.status_code == 400

# Here, you may add other tests for the remaining routes and functions
