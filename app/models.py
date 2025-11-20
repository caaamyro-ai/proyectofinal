# Este archivo define las tablas para los hábitos de la base de datos
# Ahora tenemos 3 tablas:
# 1. DailyHabit:Hábitos diarios
# 2. WeeklyHabit: Hábitos semanales (con días seleccionados)
# 3. WeeklyHabitCompletion: Nuevo modelo para guardar los días completados

# Este tercer modelo nos permitirá generar estadísticas semanales, mensuales y anuales.
# A diferencia del modelo WeeklyHabit, aquí se guarda CADA VEZ que el usuario marca un día como completado.
# Esto es esencial para generar métricas: porcentajes, rachas, totales por mes, etc.

from app import db # Importa la base de datos inicializada en __init__.py
from datetime import date   # Necesario para guardar fechas de completación



#  1) HÁBITOS DIARIOS
class DailyHabit(db.Model):

    __tablename__ = "daily_habits" 

    id = db.Column(db.Integer, primary_key=True)  # identificador único 
    name = db.Column(db.String(100), nullable=False)  # nombre del hábito (obligatorio)

    completed = db.Column(db.Boolean, default=False)
    # por ahora solo guarda si está o no completado ese día, por default no

# 2) HÁBITOS SEMANALES 
class WeeklyHabit(db.Model):

    __tablename__ = "weekly_habits"

    id = db.Column(db.Integer, primary_key=True)  # identificador único

    name = db.Column(db.String(100), nullable=False)  # nombre del hábito
    completed = db.Column(db.Boolean, default=False)
    #  lo dejamos para compatibilidad con el frontend actual
    # En el futuro lo eliminaremos cuando movamos todo a WeeklyHabitCompletion.

    # Días seleccionados por el usuario para este hábito
    # Se almacenan como un string tipo: "mon,tue,thu"
    days = db.Column(db.String(50), nullable=False)
    # NOTA: days NOOO puede quedar vacío o el hábito no tendría sentido.

# 3) NUEVO MODELO: REGISTROS REALES DE COMPLETACIÓN DIARIA
# Este modelo permite almacenar los días en que el usuario marcó un hábito semanal como completado.
# aquí se guardará una fila cuando el usuario marque COMPLETADO un día específico
class WeeklyHabitCompletion(db.Model):

    __tablename__ = "weekly_habit_completion"

    id = db.Column(db.Integer, primary_key=True)

    # Relación con WeeklyHabit: cada registro pertenece a un hábito
    weekly_habit_id = db.Column(
        db.Integer,
        db.ForeignKey("weekly_habits.id"),
        nullable=False
    )

    # Fecha exacta en que el usuario marcó completado
    date = db.Column(
        db.Date,
        default=date.today,
        nullable=False
    )

    # Booleano para permitir marcar/desmarcar
    completed = db.Column(db.Boolean, default=True)

    # Esto permite acceder desde WeeklyHabit a sus registros con
    # habit.completions: lista de objetos WeeklyHabitCompletion
    habit = db.relationship("WeeklyHabit", backref="completions")
    # backref crea automáticamente una relación inversa útil para estadísticas
