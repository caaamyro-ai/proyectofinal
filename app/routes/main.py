# este archivo contiene solo rutas principales
# las rutas de estadísticas están separadas para mantener el proyecto limpio.

from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from ..models import DailyHabit, WeeklyHabit
from datetime import datetime, timedelta

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
    habit.completed_at = datetime.now() if habit.completed else None

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

# CALENDARIO
@main.route("/calendar")
def calendar():
    from calendar import month_name
    
    # Obtener año y mes de los parámetros o usar actual
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)
    
    # Nombre del mes en español
    month_names_es = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    current_month = f"{month_names_es[month]} {year}"
    
    # Obtener datos de hábitos completados
    habit_completions = get_calendar_data(year, month)
    
    return render_template("calendar.html",
                         current_month=current_month,
                         year=year,
                         month=month,
                         habit_completions=habit_completions)

# ============================================
# FUNCIONES AUXILIARES PARA ANALYTICS
# ============================================

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

# ANÁLISIS
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
    
    # Obtener progreso individual
    habit_progress = get_habit_progress_list()
    
    # Obtener actividad semanal - ESTA LÍNEA ES CRÍTICA
    week_activity = get_week_activity()

    return render_template("analytics.html", 
                         total_habits=total_habits,
                         current_streak=current_streak,
                         completion_rate=completion_rate,
                         best_streak=best_streak,
                         habit_progress=habit_progress,
                         week_activity=week_activity)

def get_calendar_data(year, month):
    """Obtiene los hábitos completados por día para el calendario"""
    from ..models import WeeklyHabitCompletion
    from calendar import monthrange
    
    # Obtener todos los días del mes con hábitos completados
    calendar_data = {}
    
    # Obtener el rango de días del mes
    num_days = monthrange(year, month)[1]
    
    for day in range(1, num_days + 1):
        date_obj = datetime(year, month, day).date()
        
        # Contar hábitos completados ese día
        count = WeeklyHabitCompletion.query.filter_by(
            date=date_obj,
            completed=True
        ).count()
        
        if count > 0:
            date_str = date_obj.strftime('%Y-%m-%d')
            calendar_data[date_str] = count
    
    return calendar_data

def get_habit_progress_list():
    """Obtiene el progreso de cada hábito en los últimos 7 días"""
    from ..models import DailyHabit, WeeklyHabitCompletion
    
    progress_list = []
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)
    
    # Obtener todos los hábitos diarios
    daily_habits = DailyHabit.query.all()
    
    for habit in daily_habits:
        # Contar cuántos días de los últimos 7 completó este hábito
        completed = WeeklyHabitCompletion.query.filter(
            WeeklyHabitCompletion.habit_id == habit.id,
            WeeklyHabitCompletion.habit_type == "daily",
            WeeklyHabitCompletion.date.between(start_date, end_date),
            WeeklyHabitCompletion.completed == True
        ).count()
        
        total = 7  # últimos 7 días
        percentage = int((completed / total) * 100) if total > 0 else 0
        
        # Calcular racha para este hábito específico
        streak = 0
        check_date = end_date
        while True:
            has_completion = WeeklyHabitCompletion.query.filter_by(
                habit_id=habit.id,
                habit_type="daily",
                date=check_date,
                completed=True
            ).first()
            
            if has_completion:
                streak += 1
                check_date -= timedelta(days=1)
            else:
                break
        
        progress_list.append({
            'name': habit.name,
            'completed': completed,
            'total': total,
            'percentage': percentage,
            'streak': streak
        })
    
    return progress_list

def get_week_activity():
    """Obtiene la cantidad de hábitos completados por día en la última semana"""
    from ..models import WeeklyHabitCompletion
    
    end_date = datetime.now().date()
    week_data = []
    
    for i in range(6, -1, -1):  # Últimos 7 días
        date_obj = end_date - timedelta(days=i)
        count = WeeklyHabitCompletion.query.filter_by(
            date=date_obj,
            completed=True
        ).count()
        
        day_name = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'][date_obj.weekday()]
        
        week_data.append({
            'day': day_name,
            'count': count
        })
    
    return week_data