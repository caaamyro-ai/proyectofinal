from flask import Blueprint, render_template, request, redirect, url_for
# Blueprint = agrupar rutas
# render_template = mostrar HTML
# request = leer formularios
# redirect/url_for = redirecciones limpias

from .models import db, DailyHabit, WeeklyHabit, HabitCompletion
# Importamos todos los modelos, incluido el NUEVO modelo de historial de completado

#   BLUEPRINT PRINCIPAL
main = Blueprint('main', __name__)

#   INDEX: MUESTRA HÁBITOS Y SU ESTADO
@main.route('/')
def index():

    # Obtiene TODOS los hábitos diarios
    daily_habits = DailyHabit.query.all()

    # Obtiene TODOS los hábitos semanales
    weekly_habits = WeeklyHabit.query.all()

    # Para mostrar qué días se han completado (solo hoy POR AHORA)
    # Vamos a consultar por fecha de hoy
    from datetime import date
    today = date.today()

    # Cargar COMPLETADOS diarios de HOY
    daily_completed_today = {
        c.habit_id: True
        for c in HabitCompletion.query.filter_by(date=today).filter_by(type="daily").all()
    }

    # Cargar COMPLETADOS semanales de HOY
    weekly_completed_today = {
        (c.habit_id, c.day): True
        for c in HabitCompletion.query.filter_by(date=today).filter_by(type="weekly").all()
    }

    return render_template(
        'index.html',
        daily_habits=daily_habits,
        weekly_habits=weekly_habits,
        daily_completed_today=daily_completed_today,
        weekly_completed_today=weekly_completed_today
    )

#   AGREGAR HÁBITO DIARIO
@main.route('/add/daily', methods=['POST'])
def add_daily_habit():
    name = request.form.get('name')

    # Validación: nombre vacío
    if not name or name.strip() == "":
        return "Error: el nombre del hábito diario no puede estar vacío", 400

    # Validación: duplicado
    existing = DailyHabit.query.filter_by(name=name).first()
    if existing:
        return "Error: Ya existe un hábito diario con ese nombre.", 409

    new_habit = DailyHabit(name=name)
    db.session.add(new_habit)
    db.session.commit()

    return redirect(url_for('main.index'))


#   AGREGAR HÁBITO SEMANAL
@main.route('/add/weekly', methods=['POST'])
def add_weekly_habit():

    name = request.form.get('name')
    days_selected = request.form.getlist('days')  # lista de checkboxes marcados

    # Validación: sin nombre
    if not name or name.strip() == "":
        return "Error: el nombre del hábito semanal no puede estar vacío", 400

    # Validación duplicado
    existing = WeeklyHabit.query.filter_by(name=name).first()
    if existing:
        return "Error: Ya existe un hábito semanal con ese nombre.", 409

    # Validación: sin días
    if not days_selected:
        return "Error: debes seleccionar al menos un día para este hábito semanal.", 400

    # Convertimos lista: string "mon,wed,fri"
    days_string = ",".join(days_selected)

    new_habit = WeeklyHabit(name=name, days=days_string)
    db.session.add(new_habit)
    db.session.commit()

    return redirect(url_for('main.index'))

#   COMPLETAR HÁBITO DIARIO (con HISTORIAL)
@main.route('/complete/daily/<int:habit_id>', methods=['POST'])
def complete_daily(habit_id):

    from datetime import date
    today = date.today()

    # ¿Existe ya un registro de completado HOY?
    existing = HabitCompletion.query.filter_by(
        habit_id=habit_id,
        type="daily",
        date=today
    ).first()

    if existing:
        # Si ya estaba completado hoy = lo DESMARCA
        db.session.delete(existing)
    else:
        # Crear registro nuevo para hoy
        c = HabitCompletion(
            habit_id=habit_id,
            type="daily",
            day=None,        # no aplica para hábitos diarios
            date=today
        )
        db.session.add(c)

    db.session.commit()
    return redirect(url_for('main.index'))

#   COMPLETAR HÁBITO SEMANAL POR DÍA
#   (ESTADO REAL con HISTORIAL y por cada día)
@main.route('/complete/weekly/<int:habit_id>/<day>', methods=['POST'])
def complete_weekly(habit_id, day):

    from datetime import date
    today = date.today()

    # Primero verificamos que el hábito existe
    habit = WeeklyHabit.query.get_or_404(habit_id)

    # Validación: ese día debe ser uno de los días configurados en el hábito
    valid_days = habit.days.split(",")
    if day not in valid_days:
        return f"Error: El hábito no está configurado para {day}.", 400

    # ¿YA existe registro de completado HOY?
    existing = HabitCompletion.query.filter_by(
        habit_id=habit_id,
        type="weekly",
        day=day,
        date=today
    ).first()

    if existing:
        # Si existe = se DESMARCA
        db.session.delete(existing)
    else:
        # Crear nuevo registro
        c = HabitCompletion(
            habit_id=habit_id,
            type="weekly",
            day=day,
            date=today
        )
        db.session.add(c)

    db.session.commit()
    return redirect(url_for('main.index'))

#   ELIMINAR HÁBITOS
@main.route('/delete/daily/<int:habit_id>', methods=['POST'])
def delete_daily(habit_id):
    habit = DailyHabit.query.get_or_404(habit_id)

    # Borrar historial asociado
    HabitCompletion.query.filter_by(habit_id=habit.id, type="daily").delete()

    db.session.delete(habit)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/delete/weekly/<int:habit_id>', methods=['POST'])
def delete_weekly(habit_id):
    habit = WeeklyHabit.query.get_or_404(habit_id)

    # Borrar historial asociado
    HabitCompletion.query.filter_by(habit_id=habit.id, type="weekly").delete()

    db.session.delete(habit)
    db.session.commit()
    return redirect(url_for('main.index'))

#   EDITAR HÁBITO DIARIO
@main.route('/edit/daily/<int:habit_id>')
def edit_daily(habit_id):
    habit = DailyHabit.query.get_or_404(habit_id)
    return render_template('edit_daily.html', habit=habit)


# Guardar cambios (diarios)
@main.route('/update/daily/<int:habit_id>', methods=['POST'])
def update_daily(habit_id):
    habit = DailyHabit.query.get_or_404(habit_id)

    new_name = request.form.get('name')

    # Validaciones
    if not new_name or new_name.strip() == "":
        return "Error: el nombre no puede estar vacío.", 400

    existing = DailyHabit.query.filter_by(name=new_name).first()
    if existing and existing.id != habit.id:
        return "Error: ya existe un hábito diario con ese nombre.", 409

    habit.name = new_name
    db.session.commit()
    return redirect(url_for('main.index'))

#   EDITAR HÁBITO SEMANAL
@main.route('/edit/weekly/<int:habit_id>')
def edit_weekly(habit_id):

    habit = WeeklyHabit.query.get_or_404(habit_id)

    selected_days = habit.days.split(",")

    return render_template('edit_weekly.html', habit=habit, selected_days=selected_days)


# Guardar cambios (semanales)
@main.route('/update/weekly/<int:habit_id>', methods=['POST'])
def update_weekly(habit_id):

    habit = WeeklyHabit.query.get_or_404(habit_id)

    new_name = request.form.get('name')
    new_days = request.form.getlist('days')

    if not new_name or new_name.strip() == "":
        return "Error: el nombre no puede estar vacío.", 400

    existing = WeeklyHabit.query.filter_by(name=new_name).first()
    if existing and existing.id != habit.id:
        return "Error: ya existe un hábito semanal con ese nombre.", 409

    if not new_days:
        return "Error: al menos un día debe estar seleccionado.", 400

    habit.name = new_name
    habit.days = ",".join(new_days)

    db.session.commit()
    return redirect(url_for('main.index'))
