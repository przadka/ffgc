import os
from flask import Flask

def create_app():

    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')

    # The client ID and client secret from your OAuth 2.0 credentials
    app.config['CLIENT_ID'] = os.getenv('CLIENT_ID')
    app.config['CLIENT_SECRET'] = os.getenv('CLIENT_SECRET')

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import routes
    app.register_blueprint(routes.bp)

    return app

