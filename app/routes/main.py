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

#Calendario

@main.route("/calendar")
def calendar():
    return render_template("calendar.html")

# ============================================
# FUNCIONES AUXILIARES PARA ANALYTICS
# ============================================

from datetime import datetime, timedelta

def calculate_current_streak():
    """Calcula la racha actual de días consecutivos"""
    from ..models import WeeklyHabitCompletion
    
    streak = 0
    current_date = datetime.now().date()
    
    # Verificar días consecutivos hacia atrás
    while True:
        # Contar hábitos completados en esta fecha
        count = WeeklyHabitCompletion.query.filter_by(
            date=current_date,
            completed=True
        ).count()
        
        if count > 0:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    
    return streak


def calculate_weekly_completion_rate():
    """Calcula el porcentaje de hábitos completados en los últimos 7 días"""
    from ..models import DailyHabit, WeeklyHabitCompletion
    
    # Total de hábitos activos
    total_daily = DailyHabit.query.count()
    
    if total_daily == 0:
        return 0
    
    # Hábitos que deberían haberse completado en 7 días
    total_possible = total_daily * 7
    
    # Contar completados en los últimos 7 días
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)
    
    completed = WeeklyHabitCompletion.query.filter(
        WeeklyHabitCompletion.date.between(start_date, end_date),
        WeeklyHabitCompletion.completed == True,
        WeeklyHabitCompletion.habit_type == "daily"
    ).count()
    
    return int((completed / total_possible) * 100) if total_possible > 0 else 0


def calculate_best_streak():
    """Calcula la mejor racha histórica"""
    from ..models import WeeklyHabitCompletion
    
    # Obtener todas las fechas con hábitos completados, ordenadas
    dates = WeeklyHabitCompletion.query.with_entities(
        WeeklyHabitCompletion.date
    ).filter_by(completed=True).distinct().order_by(
        WeeklyHabitCompletion.date
    ).all()
    
    if not dates:
        return 0
    
    best_streak = 1
    current_streak = 1
    
    for i in range(1, len(dates)):
        prev_date = dates[i-1][0]
        curr_date = dates[i][0]
        
        # Si son días consecutivos
        if (curr_date - prev_date).days == 1:
            current_streak += 1
            best_streak = max(best_streak, current_streak)
        else:
            current_streak = 1
    
    return best_streak

#Análisis
@main.route("/analytics")
def analytics():
    # Contar hábitos totales
    daily_count = DailyHabit.query.count()
    weekly_count = WeeklyHabit.query.count()
    total_habits = daily_count + weekly_count
    
    # Calcular estadísticas
    current_streak = calculate_current_streak()
    completion_rate = calculate_weekly_completion_rate()
    best_streak = calculate_best_streak()
    
    return render_template("analytics.html", 
                         total_habits=total_habits,
                         current_streak=current_streak,
                         completion_rate=completion_rate,
                         best_streak=best_streak)