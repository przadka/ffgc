import pytest
from app import create_app

@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_index(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome to my app!" in response.data

def test_authorize_redirect(test_client):
    response = test_client.get('/authorize', follow_redirects=False)
    assert response.status_code == 302

def test_oauth2callback_without_code(test_client):
    response = test_client.get('/oauth2callback')
    assert response.status_code == 400
