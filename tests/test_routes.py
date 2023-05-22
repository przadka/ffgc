from app import create_app

def test_index():
    app = create_app()
    client = app.test_client()

    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to my app!" in response.data


def test_authorize_redirect():
    app = create_app()
    client = app.test_client()

    response = client.get('/authorize', follow_redirects=False)
    assert response.status_code == 302

def test_oauth2callback_without_code():
    app = create_app()
    client = app.test_client()

    response = client.get('/oauth2callback')
    assert response.status_code == 400