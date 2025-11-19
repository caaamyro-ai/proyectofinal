from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # Extensión que conecta Flask con la base de datos

# Crear primero la instancia global de la base de datos
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos: usa SQLite y crea habits.db en la carpeta del proyecto
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # evita advertencias innecesarias

    # Vincular la base de datos a la aplicación
    db.init_app(app)

    # IMPORTANTE:
    # Se importan los modelos aquí para evitar errores de referencia circular.
    # Ahora importamos DailyHabit y WeeklyHabit, porque Habit ya NO existe.
    from .models import DailyHabit, WeeklyHabit

    # Importar rutas después de crear la app y después de importar los modelos
    from .routes import main
    app.register_blueprint(main)

    # Crear tablas dentro del contexto de la aplicación
    with app.app_context():
        db.create_all()  # crea daily_habits y weekly_habits si no existen

    return app

