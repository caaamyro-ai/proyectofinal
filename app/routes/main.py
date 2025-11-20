
# este archivo contiene solo rutas principales
# las rutas de estadísticas están separadas para mantener el proyecto limpio.

from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from ..models import DailyHabit, WeeklyHabit

main = Blueprint("main", __name__)

# PÁGINA PRINCIPAL
@main.route("/")
def index():
    daily = DailyHabit.query.all()
    weekly = WeeklyHabit.query.all()
    return render_template("index.html", daily=daily, weekly=weekly)

# HÁBITOS DIARIOS
@main.route("/add_daily", methods=["POST"])
def add_daily_habit():
    name = request.form.get("name")

    new_habit = DailyHabit(name=name)
    db.session.add(new_habit)
    db.session.commit()

    return redirect(url_for("main.index"))


@main.route("/toggle_daily/<int:habit_id>", methods=["POST"])
def toggle_daily(habit_id):
    habit = DailyHabit.query.get(habit_id)

    habit.completed = not habit.completed

    # Si se completa entonces registrar fecha
    from datetime import datetime
    habit.completed_at = datetime.utcnow() if habit.completed else None

    db.session.commit()
    return redirect(url_for("main.index"))


@main.route("/delete_daily/<int:habit_id>", methods=["POST"])
def delete_daily(habit_id):
    habit = DailyHabit.query.get(habit_id)
    db.session.delete(habit)
    db.session.commit()
    return redirect(url_for("main.index"))

# HÁBITOS SEMANALES
@main.route("/add_weekly_habit", methods=["POST"])
def add_weekly_habit():
    name = request.form.get("name")
    selected_days = request.form.getlist("days")

    # Guardamos el string
    days_string = ",".join(selected_days)

    new_habit = WeeklyHabit(name=name, days=days_string)
    db.session.add(new_habit)
    db.session.commit()

    return redirect(url_for("main.index"))


@main.route("/delete_weekly/<int:habit_id>", methods=["POST"])
def delete_weekly(habit_id):
    habit = WeeklyHabit.query.get(habit_id)
    db.session.delete(habit)
    db.session.commit()
    return redirect(url_for("main.index"))
