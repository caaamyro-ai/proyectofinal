# estas rutas escriben en WeeklyHabitCompletion para tener estadísticas reales.
# este archivo se encarga SOLO del registro histórico, para mantener orden.

from flask import Blueprint, redirect, url_for
from app import db
from ..models import DailyHabit, WeeklyHabit, WeeklyHabitCompletion
from datetime import datetime, timezone  # Aconsejable x la zona horaria

# Blueprint exclusivo para todo lo relacionado con el LOG de hábitos
logs = Blueprint("logs", __name__)

# REGISTRO DE HÁBITOS DIARIOS

# Esta ruta alterna el estado del hábito diario (completado/no completado)
# y además registra la fecha en WeeklyHabitCompletion para estadísticas reales
#  esta ruta NO renderice templates, su función es SOLO registrar
@logs.route("/log_daily/<int:habit_id>", methods=["POST"])
def log_daily(habit_id):

    habit = DailyHabit.query.get(habit_id)

    # Invertimos el estado del hábito
    habit.completed = not habit.completed

    # Guardamos fecha solo si está marcado como completado
    habit.completed_at = datetime.now(timezone.utc) if habit.completed else None

    # Registrar en WeeklyHabitCompletion únicamente si se marcó como completado
    if habit.completed:
        entry = WeeklyHabitCompletion(
            habit_id=habit.id,
            habit_type="daily",                   # Para distinguir diario vs semanal
            date=datetime.now(timezone.utc).date() # Guardamos SOLO la fecha
        )
        db.session.add(entry)

    db.session.commit()
    return redirect(url_for("main.index"))

# REGISTRO DE HÁBITOS SEMANALES

# NO modifica un estado booleano, porque los hábitos semanales
# se contabilizan como "día cumplido" cada vez que el usuario presiona el botón
@logs.route("/log_weekly/<int:habit_id>", methods=["POST"])
def log_weekly(habit_id):

    habit = WeeklyHabit.query.get(habit_id)

    # **********NUEVO CAMBIO: obtiene el día enviado por los checkboxes*******
    # (si viene desde daily no llegará, está bien)
    day = request.form.get("day")


    # *******NUEVO CAMBIO: Registrar la fecha real de cumplimiento********
    # en WeeklyHabitCompletion usando el modelo actual
    completion = WeeklyHabitCompletion(
        habit_id=habit.id, #CAMBIO AQUÍ POR INCONSISTENCIA EN EL MODELO
        date=datetime.now(timezone.utc).date(),
        completed=True
    )

    db.session.add(completion)
    db.session.commit()

    return redirect(url_for("main.index"))