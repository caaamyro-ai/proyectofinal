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
    # Ahora importamos DailyHabit, WeeklyHabit y WeeklyLog.
    from .models import DailyHabit, WeeklyHabit, WeeklyLog


    # Rutas principales: agregar, editar, borrar, listar hábitos
    from .routes_main import main

    # Rutas para registrar los días completados del hábito semanal
    from .routes_logs import logs

    # Rutas para estadísticas (semanales, mensuales, anuales)
    from .routes_stats import stats

    # Registrar todos los blueprints en la aplicación
    app.register_blueprint(main)
    app.register_blueprint(logs)
    app.register_blueprint(stats)

    # Crear tablas dentro del contexto de la aplicación
    with app.app_context():
        db.create_all()  # crea todas las tablas si no existen (daily, weekly, weekly_logs)

    return app