# Este archivo hace las tablas para los hábitos de la base de datos (puse 2, una para hábitos diarios y otra semanal)

from . import db  # Importa la base de datos inicializada en __init__.py
# Hábitos Diarios
class DailyHabit(db.Model):

    # Esta tabla almacena hábitos que deben completarse todos los días.
    __tablename__ = "daily_habits"  # nombre explícito de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)  # identificador único, columna entera (integer)
    name = db.Column(db.String(100), nullable=False)  # nombre del hábito, nullable = false indica que no puede quedar vacío (es obligatorio)
    completed = db.Column(db.Boolean, default=False)  # si está completado o no
    # primary_key=True significa que este campo será el identificador único de cada registro 
    
    
# Hábitos Semanales
class WeeklyHabit(db.Model):
   # Esta tabla almacena hábitos que se repiten ciertos días de la semana
    __tablename__ = "weekly_habits"

    id = db.Column(db.Integer, primary_key=True)  # identificador único

    name = db.Column(db.String(100), nullable=False)  # nombre del hábito
    completed = db.Column(db.Boolean, default=False)  # marcado como completado

    # Aquí se guardan los días seleccionados para este hábito
    # Se almacenan como un string tipo: "mon,tue,thu"
    days = db.Column(db.String(50), nullable=False)  
    # NOTA: days NUNCA debe quedar vacío, sino no tendría sentido un hábito semanal

# Esto crea ambas tablas nuevas en SQLite
