# este archivo contiene solo rutas principales
# las rutas de estadísticas están separadas para mantener el proyecto limpio.

from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from ..models import DailyHabit, WeeklyHabit
from datetime import datetime

main = Blueprint("main", __name__)

# PÁGINA PRINCIPAL
@main.route("/")
def index():
    daily = DailyHabit.query.all()
    weekly = WeeklyHabit.query.all()
    return render_template("index.html", daily=daily, weekly=weekly)

# HÁBITOS DIARIOS

# Crear hábito diario
@main.route("/add_daily", methods=["POST"])
def add_daily_habit():
    name = request.form.get("name")

    new_habit = DailyHabit(name=name)
    db.session.add(new_habit)
    db.session.commit()

    return redirect(url_for("main.index"))

# Marcar o desmarcar hábito diario
@main.route("/toggle_daily/<int:habit_id>", methods=["POST"])
def toggle_daily(habit_id):
    habit = DailyHabit.query.get(habit_id)

    habit.completed = not habit.completed

    # Si se completa entonces registrar fecha
    habit.completed_at = datetime.utcnow() if habit.completed else None

    db.session.commit()
    return redirect(url_for("main.index"))

# Editar hábito diario
@main.route("/edit_daily/<int:habit_id>", methods=["GET", "POST"])
def edit_daily(habit_id):
    habit = DailyHabit.query.get(habit_id)

    if request.method == "POST":
        new_name = request.form.get("name")
        habit.name = new_name
        db.session.commit()
        return redirect(url_for("main.index"))

    return render_template("edit_daily.html", habit=habit)

# Eliminar hábito diario
@main.route("/delete_daily/<int:habit_id>", methods=["POST"])
def delete_daily(habit_id):
    habit = DailyHabit.query.get(habit_id)
    db.session.delete(habit)
    db.session.commit()
    return redirect(url_for("main.index"))

# HÁBITOS SEMANALES

# Crear hábito semanal
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

# Editar hábito semanal
@main.route("/edit_weekly/<int:habit_id>", methods=["GET", "POST"])
def edit_weekly(habit_id):
    habit = WeeklyHabit.query.get(habit_id)

    if request.method == "POST":
        new_name = request.form.get("name")
        new_days = request.form.getlist("days")

        habit.name = new_name
        habit.days = ",".join(new_days)

        db.session.commit()
        return redirect(url_for("main.index"))

    # Convertir string de días en lista para el formulario
    selected_days = habit.days.split(",") if habit.days else []

    return render_template("edit_weekly.html", habit=habit, selected_days=selected_days)

# Eliminar hábito semanal
@main.route("/delete_weekly/<int:habit_id>", methods=["POST"])
def delete_weekly(habit_id):
    habit = WeeklyHabit.query.get(habit_id)
    db.session.delete(habit)
    db.session.commit()
    return redirect(url_for("main.index"))
