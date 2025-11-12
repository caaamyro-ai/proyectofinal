from flask import Blueprint, render_template,  request, redirect, url_for
from .models import db, Habit  # Importa el modelo de la base de datos

# Definir un "blueprint" para las rutas principales
main = Blueprint('main', __name__)

# muestra los hábitos
@main.route('/')
def index():
    # Obtiene todos los hábitos de la base de datos tabla habit
    habits = Habit.query.all()
    return render_template('index.html', habits=habits)  # envía los datos a la plantilla index

# agrega una ruta para agregar hábitos
@main.route('/add', methods=['POST']) # ruta para enviar los datos tipo POST (envía datos desde el servidor)
def add_habit():
    name = request.form.get('name')  #Aquí Flask recoge los datos del formulario HTML, el form debe tener una entrada name
    if name:  # Verifica que el campo no esté vacío
        new_habit = Habit(name=name) # Crea un nuevo objeto Habit
        db.session.add(new_habit) # Agrega el nuevo hábito a la sesión de SQLAlchemy (como un "borrador")
        db.session.commit()  # guarda los datos en la base 
    return redirect(url_for('main.index')) # redirije a la página principal

# Para marcar hábitos como completados 
@main.route('/complete/<int:habit_id>', methods=['POST'])  # c/hábito tiene su propio id, y <int:habit_id> permite capturar ese n° desde la url 
def complete_habit(habit_id):
    habit = Habit.query.get(habit_id)   # Busca el hábito en la base de datos según su ID
    if habit:
        habit.completed = True  # Cambia el valor de completed a True
        db.session.commit()  # Guarda los cambios en la base de datos
    return redirect(url_for('main.index'))  # Redirige al usuario de nuevo a la página principal