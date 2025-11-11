from flask import Blueprint, render_template,  request, redirect, url_for
from .models import db, Habit  # Importa el modelo de la base de datos

# Definir un "blueprint" para las rutas principales
main = Blueprint('main', __name__)

# muestra los hábitos
@main.route('/')
def index():
    # Obtiene todos los hábitos de la base de datos tabla habit
    habits = Habit.query.all()
    return render_template('index.html', habits=habits) # envía los datos a la plantilla index

# agrega una ruta para agregar hábitos
@main.route('/add', methods=['POST']) # ruta para enviar los datos tipo POST (envía datos desde el servidor)
def add_habit():
    habit_name = request.form.get('name')  # toma el dato del formulario HTML
    if habit_name:  # si el usuario escribió algo
        new_habit = Habit(name=habit_name)
        db.session.add(new_habit)
        db.session.commit()
    return redirect(url_for('main.index'))  # redirige a la página principal