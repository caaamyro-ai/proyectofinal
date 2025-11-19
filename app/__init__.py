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

    # Importar modelos (IMPORTANTÍSIMO: hacer esto después de crear db)
    from .models import DailyHabit, WeeklyHabit, WeeklyHabitCompletion

    # Importar rutas
    from .routes.main import main
    from .routes.logs import logs
    from .routes.stats import stats

    # Registrar blueprints
    app.register_blueprint(main)
    app.register_blueprint(logs)
    app.register_blueprint(stats)

    # Crear tablas dentro del contexto de la aplicación
    with app.app_context():
        db.create_all()

    return app