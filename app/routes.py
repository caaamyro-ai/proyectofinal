from flask import Blueprint, render_template, request, redirect, url_for  
# para manejar rutas, formularios y redirecciones

from .models import db, DailyHabit, WeeklyHabit  
# Importa los modelos de hábitos diarios y semanales


# Definir un "blueprint" para las rutas principales
main = Blueprint('main', __name__)


#  Mostrar TODOS los hábitos (diarios y semanales separados)
@main.route('/')  # ruta raíz
def index():

    # Obtiene TODOS los hábitos diarios
    daily_habits = DailyHabit.query.all()

    # Obtiene TODOS los hábitos semanales
    weekly_habits = WeeklyHabit.query.all()

    # Renderiza index.html y le envía ambas listas separadas
    return render_template(
        'index.html',
        daily_habits=daily_habits,
        weekly_habits=weekly_habits
    )

#  AGREGAR hábito diario
@main.route('/add/daily', methods=['POST'])
def add_daily_habit():
    name = request.form.get('name')

    # Validación: nombre vacío
    if not name or name.strip() == "":
        return "Error: el nombre del hábito diario no puede estar vacío", 400

    # Validación: nombre duplicado dentro de DailyHabit
    existing = DailyHabit.query.filter_by(name=name).first()
    if existing:
        return "Error: Ya existe un hábito diario con ese nombre.", 409

    # Crear el nuevo hábito
    new_habit = DailyHabit(name=name)
    db.session.add(new_habit)
    db.session.commit()

    return redirect(url_for('main.index'))

#  AGREGAR hábito semanal (con días)
@main.route('/add/weekly', methods=['POST'])
def add_weekly_habit():

    name = request.form.get('name')
    days_selected = request.form.getlist('days')  # lista de checkboxes marcados

    # Validación: nombre vacío
    if not name or name.strip() == "":
        return "Error: el nombre del hábito semanal no puede estar vacío", 400

    # Validación: duplicado
    existing = WeeklyHabit.query.filter_by(name=name).first()
    if existing:
        return "Error: Ya existe un hábito semanal con ese nombre.", 409

    # Validación: debe tener al menos un día
    if not days_selected:
        return "Error: Debes seleccionar al menos un día para este hábito semanal.", 400

    # Convertimos ["mon","wed","fri"] -> "mon,wed,fri"
    days_string = ",".join(days_selected)

    new_habit = WeeklyHabit(name=name, days=days_string)
    db.session.add(new_habit)
    db.session.commit()

    return redirect(url_for('main.index'))

#  Completar o desmarcar hábito diario
@main.route('/complete/daily/<int:habit_id>', methods=['POST'])
def complete_daily(habit_id):
    habit = DailyHabit.query.get_or_404(habit_id)
    habit.completed = not habit.completed  # alterna True/False
    db.session.commit()
    return redirect(url_for('main.index'))

# Completar hábito semanal por DÍA INDIVIDUAL
@main.route('/complete/weekly/<int:habit_id>/<day>', methods=['POST'])
def complete_weekly(habit_id, day):
    
    # Esta ruta permitirá marcar como completado un hábito semanal
    # por un día específico (ej: lunes, martes, etc)
    
    habit = WeeklyHabit.query.get_or_404(habit_id)

    # Aquí por ahora solo alternamos completed general,
    # luego se puede ampliar para llevar un registro por día
    habit.completed = not habit.completed
    db.session.commit()

    return redirect(url_for('main.index'))

#  ELIMINAR hábito diario
@main.route('/delete/daily/<int:habit_id>', methods=['POST'])
def delete_daily(habit_id):
    habit = DailyHabit.query.get_or_404(habit_id)
    db.session.delete(habit)
    db.session.commit()
    return redirect(url_for('main.index'))

#  ELIMINAR hábito semanal
@main.route('/delete/weekly/<int:habit_id>', methods=['POST'])
def delete_weekly(habit_id):
    habit = WeeklyHabit.query.get_or_404(habit_id)
    db.session.delete(habit)
    db.session.commit()
    return redirect(url_for('main.index'))

#  Mostrar formulario de edición (diarios)
@main.route('/edit/daily/<int:habit_id>')
def edit_daily(habit_id):
    habit = DailyHabit.query.get_or_404(habit_id)
    return render_template('edit_daily.html', habit=habit)

# 📌 Guardar cambios de hábito diario
@main.route('/update/daily/<int:habit_id>', methods=['POST'])
def update_daily(habit_id):
    habit = DailyHabit.query.get_or_404(habit_id)

    new_name = request.form.get('name')

    # Validación: vacío
    if not new_name or new_name.strip() == "":
        return "Error: el nombre no puede estar vacío.", 400

    # Validación duplicado
    existing = DailyHabit.query.filter_by(name=new_name).first()
    if existing and existing.id != habit.id:
        return "Error: Ya existe un hábito diario con ese nombre.", 409

    habit.name = new_name
    db.session.commit()

    return redirect(url_for('main.index'))

#  Mostrar formulario de edición (semanales)
@main.route('/edit/weekly/<int:habit_id>')
def edit_weekly(habit_id):
    habit = WeeklyHabit.query.get_or_404(habit_id)

    # Convertimos string "mon,tue" en lista ["mon", "tue"]
    selected_days = habit.days.split(",")

    return render_template('edit_weekly.html', habit=habit, selected_days=selected_days)

#  Guardar cambios en hábito semanal
@main.route('/update/weekly/<int:habit_id>', methods=['POST'])
def update_weekly(habit_id):
    habit = WeeklyHabit.query.get_or_404(habit_id)

    new_name = request.form.get('name')
    new_days = request.form.getlist('days')

    # Validación nombre vacío
    if not new_name or new_name.strip() == "":
        return "Error: el nombre no puede estar vacío.", 400

    # Validación duplicado
    existing = WeeklyHabit.query.filter_by(name=new_name).first()
    if existing and existing.id != habit.id:
        return "Error: Ya existe un hábito semanal con ese nombre.", 409

    # Validación días vacíos
    if not new_days:
        return "Error: al menos un día debe estar seleccionado.", 400

    habit.name = new_name
    habit.days = ",".join(new_days)

    db.session.commit()

    return redirect(url_for('main.index'))
