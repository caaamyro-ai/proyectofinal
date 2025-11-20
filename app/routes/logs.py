# estas rutas escriben en WeeklyHabitCompletion para tener estadísticas reales.
# este archivo se encarga SOLO del registro histórico, para mantener orden.

from flask import Blueprint, redirect, url_for
from app import db
from ..models import DailyHabit, WeeklyHabit, WeeklyHabitCompletion
from datetime import datetime, timezone # Aconsejable para que tome la zona horaria

logs = Blueprint("logs", __name__)

# Registrar completado de hábito diario
@logs.route("/log_daily/<int:habit_id>", methods=["POST"])
def log_daily(habit_id):

    habit = DailyHabit.query.get(habit_id)
    habit.completed = not habit.completed
    habit.completed_at = datetime.now(timezone.utc) if habit.completed else None

    # Registrar en WeeklyHabitCompletion si se completa
    if habit.completed:
        entry = WeeklyHabitCompletion(
            habit_id=habit.id,
            habit_type="daily",
            date=datetime.now(timezone.utc).date()
        )
        db.session.add(entry)

    db.session.commit()
    return redirect(url_for("main.index"))

# Registrar día completado en hábito semanal
@logs.route("/log_weekly/<int:habit_id>", methods=["POST"])
def log_weekly(habit_id):

    habit = WeeklyHabit.query.get(habit_id)

    # Registrar día actual
    habit.completed_at = datetime.now(timezone.utc)

    entry = WeeklyHabitCompletion(
        habit_id=habit.id,
        habit_type="weekly",
        date=datetime.now(timezone.utc).date()
    )
    db.session.add(entry)

    db.session.commit()
    return redirect(url_for("main.index"))
