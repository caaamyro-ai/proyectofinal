# Este archivo define las tablas para los hábitos de la base de datos
# Ahora tenemos 3 tablas:
# 1. DailyHabit: Hábitos diarios
# 2. WeeklyHabit: Hábitos semanales (con días seleccionados)
# 3. WeeklyHabitCompletion: Nuevo modelo para guardar los días completados

# Este tercer modelo nos permitirá generar estadísticas semanales, mensuales y anuales.

from app import db  # Importa la base de datos inicializada en __init__.py
from datetime import date   # Necesario para guardar fechas de completación

#  1) HÁBITOS DIARIOS
class DailyHabit(db.Model):

    __tablename__ = "daily_habits"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    completed = db.Column(db.Boolean, default=False)
    # por ahora solo guarda si está o no completado ese día, por default no


#  2) HÁBITOS SEMANALES
class WeeklyHabit(db.Model):

    __tablename__ = "weekly_habits"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Mantengo este booleano por compatibilidad con la UI actual
    completed = db.Column(db.Boolean, default=False)

    # Días seleccionados por el usuario para este hábito
    # Se almacenan como string tipo: "mon,tue,thu"
    days = db.Column(db.String(50), nullable=False)
    # IMPORTANTE: no debe quedar vacío.

#  3) REGISTRO REAL DE CADA DÍA COMPLETADO
class WeeklyHabitCompletion(db.Model):

    __tablename__ = "weekly_habit_completion"

    id = db.Column(db.Integer, primary_key=True)

    # ID del hábito (puede ser diario o semanal)
    habit_id = db.Column(db.Integer, nullable=False)
    
    # Tipo de hábito: "daily" o "weekly"
    habit_type = db.Column(db.String(10), nullable=False)

    # Fecha exacta en que el usuario marcó este día como completado
    date = db.Column(db.Date, default=date.today, nullable=False)

    # Booleano para permitir marcar/desmarcar
    completed = db.Column(db.Boolean, default=True)
