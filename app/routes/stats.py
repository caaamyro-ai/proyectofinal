# Consultas SQL y rutas para estadísticas semanales, mensuales y anuales
# separamos todo en este archivo porque en el futuro pueden crecer mucho

from flask import Blueprint, jsonify
from ..models import WeeklyHabitCompletion
from datetime import datetime, timedelta, timezone
from sqlalchemy import func

stats = Blueprint("stats", __name__)

# Estadísticas de la semana actual
@stats.route("/stats/weekly")
def stats_weekly():

    today = datetime.now(timezone.utc).date()
    start_week = today - timedelta(days=today.weekday())  # lunes

    results = WeeklyHabitCompletion.query.filter(
        WeeklyHabitCompletion.date >= start_week
    ).count()

    return jsonify({
        "period": "weekly",
        "start": str(start_week),
        "completed": results
    })

# Estadísticas del mes
@stats.route("/stats/monthly")
def stats_monthly():

    today = datetime.now(timezone.utc).date()
    start_month = today.replace(day=1)

    results = WeeklyHabitCompletion.query.filter(
        WeeklyHabitCompletion.date >= start_month
    ).count()

    return jsonify({
        "period": "monthly",
        "start": str(start_month),
        "completed": results
    })

# Estadísticas del año
@stats.route("/stats/yearly")
def stats_yearly():

    today = datetime.now(timezone.utc).date()
    start_year = today.replace(month=1, day=1)

    results = WeeklyHabitCompletion.query.filter(
        WeeklyHabitCompletion.date >= start_year
    ).count()

    return jsonify({
        "period": "yearly",
        "start": str(start_year),
        "completed": results
    })
