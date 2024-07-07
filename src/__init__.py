""" Initialize the Flask app. """

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy  # Importar SQLAlchemy
from flask_migrate import Migrate # Importar Flask migrate
from src.persistence.repository import RepositoryManager
from src.config import get_config
from dotenv import load_dotenv

cors = CORS()
repo = RepositoryManager()
db = SQLAlchemy()  # Inicializa SQLAlchemy
load_dotenv() # Inicializa para cargar variables de entorno desde el archivo ".env"
migrate = Migrate()

def create_app(config_class="src.config.DevelopmentConfig") -> Flask:
    """
    Create a Flask app with the given configuration class.
    The default configuration class is DevelopmentConfig.
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    app.config.from_object(config_class)

    register_extensions(app)
    register_routes(app)
    register_handlers(app)

    print(f"Using {repo.repo} repository")

    return app


def register_extensions(app: Flask) -> None:
    """Register the extensions for the Flask app"""
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    repo.init_app(app)
    db.init_app(app)  # inicializa db
    migrate.init_app(app, db)  # Inicializa Flask-Migrate con la app y db
    with app.app_context():  # Crear todas las tablas necesarias en la base de datos
        db.create_all()

def register_routes(app: Flask) -> None:
    """Import and register the routes for the Flask app"""

    # Import the routes here to avoid circular imports
    from src.api import api_bp

    # Register the blueprints in the app
    app.register_blueprint(api_bp)


def register_handlers(app: Flask) -> None:
    """Register the error handlers for the Flask app."""
    app.errorhandler(404)(lambda e: ({"error": "Not found", "message": str(e)}, 404))
    app.errorhandler(400)(lambda e: ({"error": "Bad request", "message": str(e)}, 400))
