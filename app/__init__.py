from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # NUEVO PARA MIGRACIONES

# Instancias globales
db = SQLAlchemy()
migrate = Migrate()  # NUEVO PARA MIGRACIONES

def create_app():
    app = Flask(__name__)

    # Configuración Base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar SQLAlchemy
    db.init_app(app)

    # Importar modelos (después de db.init_app)
    from .models import DailyHabit, WeeklyHabit, WeeklyHabitCompletion

    # Importar rutas
    from .routes.main import main
    from .routes.logs import logs
    from .routes.stats import stats

    # Registrar blueprints
    app.register_blueprint(main)
    app.register_blueprint(logs)
    app.register_blueprint(stats)

    # Inicializar Migraciones 
    migrate.init_app(app, db)

    return app   