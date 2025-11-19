# estas rutas escriben en HabitLog para tener estadísticas reales.
# este archivo se encarga SOLO del registro histórico, para mantener orden.

from flask import Blueprint, redirect, url_for
from . import db
from .models import DailyHabit, WeeklyHabit, HabitLog
from datetime import datetime

logs = Blueprint("logs", __name__)

# Registrar completado de hábito diario
@logs.route("/log_daily/<int:habit_id>", methods=["POST"])
def log_daily(habit_id):

    habit = DailyHabit.query.get(habit_id)
    habit.completed = not habit.completed
    habit.completed_at = datetime.utcnow() if habit.completed else None

    # Registrar en HabitLog si se completa
    if habit.completed:
        entry = HabitLog(
            habit_id=habit.id,
            habit_type="daily",
            date=datetime.utcnow().date()
        )
        db.session.add(entry)

    db.session.commit()
    return redirect(url_for("main.index"))

# Registrar día completado en hábito semanal
@logs.route("/log_weekly/<int:habit_id>", methods=["POST"])
def log_weekly(habit_id):

    habit = WeeklyHabit.query.get(habit_id)

    # Registrar día actual
    habit.completed_at = datetime.utcnow()

    entry = HabitLog(
        habit_id=habit.id,
        habit_type="weekly",
        date=datetime.utcnow().date()
    )
    db.session.add(entry)

    db.session.commit()
    return redirect(url_for("main.index"))
