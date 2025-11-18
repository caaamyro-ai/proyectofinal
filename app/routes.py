from flask import Blueprint, render_template, request, redirect, url_for  # para manejar rutas, formularios y redirecciones
from .models import db, Habit  # Importa el modelo Habit y la base de datos

# Definir un "blueprint" para las rutas principales
main = Blueprint('main', __name__)

# Mostrar hábitos
@main.route('/')  # ruta raíz
def index():
    habits = Habit.query.all()  # obtiene todos los hábitos
    return render_template('index.html', habits=habits)  # envía la lista a la plantilla

# Agregar hábitos (con validaciones)
@main.route('/add', methods=['POST'])  # acepta solo POST
def add_habit():
    name = request.form.get('name')  # obtiene el campo del formulario

    # Validación: nombre vacío
    if not name or name.strip() == "":
        return "Error: el nombre del hábito no puede estar vacío", 400

    # Validación: hábito duplicado
    existing = Habit.query.filter_by(name=name).first()
    if existing:
        return "Error: Ya existe un hábito con ese nombre.", 409

    new_habit = Habit(name=name)  # crea el hábito
    db.session.add(new_habit)
    db.session.commit()

    return redirect(url_for('main.index'))  # redirige al inicio


# Completar o desmarcar hábito
@main.route('/complete/<int:habit_id>', methods=['POST'])
def complete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    habit.completed = not habit.completed  # alterna True/False
    db.session.commit()
    return redirect(url_for('main.index'))


# Eliminar hábito
@main.route('/delete/<int:habit_id>', methods=['POST'])
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    db.session.delete(habit)
    db.session.commit()
    return redirect(url_for('main.index'))


# Mostrar formulario de edición
@main.route('/edit/<int:habit_id>', methods=['GET'])
def edit_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)  # obtiene el hábito o 404
    return render_template('edit.html', habit=habit)  # carga la plantilla


# Guardar cambios (actualizar hábito)
@main.route('/update/<int:habit_id>', methods=['POST'])
def update_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)

    new_name = request.form.get('title')  # obtiene el nuevo nombre
    new_description = request.form.get('description')  # obtiene descripción

    # Validación: nombre vacío
    if not new_name or new_name.strip() == "":
        return "Error: El nombre no puede estar vacío.", 400

    # Validación: nombre duplicado (salvo que sea él mismo)
    existing = Habit.query.filter_by(name=new_name).first()
    if existing and existing.id != habit.id:
        return "Error: Ya existe un hábito con ese nombre.", 409

    # Actualizar valores
    habit.name = new_name
    habit.description = new_description

    db.session.commit()
    return redirect(url_for('main.index'))