from flask import Flask
from flask_sqlalchemy import SQLAlchemy # importa la extensión SQLAlchemy de Flask (conecta la app con una base de datos)

# Crear la instancia de la base de datos primero
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar la base de datos con la app
    db.init_app(app)

    # Importar aquí para evitar errores de referencia circular
    from .models import Habit
    from .routes import main
    app.register_blueprint(main)

    # Crear las tablas
    with app.app_context():
        db.create_all()

    return app
