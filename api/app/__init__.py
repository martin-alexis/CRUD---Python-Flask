from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from api.config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__,
                template_folder='../../frontend/pages',
                static_folder='../../frontend/static')
    CORS(app)
    app.config.from_object(Config)

    db.init_app(app)

    # Import and register the route blueprint
    from .routes.main_route import main_bp
    app.register_blueprint(main_bp, url_prefix='/')

    from .routes.personas_route import personas_bp
    app.register_blueprint(personas_bp, url_prefix='/')

    from .routes.usuarios_route import usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/')

    from .routes.auth_route import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/')

    return app
