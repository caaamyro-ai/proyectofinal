from flask import Blueprint, render_template,  request, redirect, url_for #para renderizar plantillas HTML render_ template
from .models import db, Habit  # Importa el modelo de la base de datos

# Definir un "blueprint" para las rutas principales
main = Blueprint('main', __name__)

# Mostrar hábitos
@main.route('/')  # registra la ruta raíz
def index():
    habits = Habit.query.all()  # usa SQLAlchemy para obtener todos los registros de la tabla Habit
    return render_template('index.html', habits=habits) # renderiza la plantilla index.html y le pasa la lista habits para que el HTML la muestre


# Agregar hábitos (con validaciones)
@main.route('/add', methods=['POST'])  # acepta solo POST
def add_habit():
    name = request.form.get('name') # obtiene el campo name del formulario enviado.

    # Validación: nombre vacío
    if not name or name.strip() == "":
        return "Error: el nombre del hábito no puede estar vacío", 400 # si el usuario envía solo espacios o nada, devuelves error HTTP 400 (Bad Request) con un mensaje

    # Validación: hábito duplicado
    existing = Habit.query.filter_by(name=name).first()
    if existing:
        return "Error: Ya existe un hábito con ese nombre.", 409 # buscas si ya existe un hábito con ese name. Si existe, devuelves 409 (Conflict)
#agregas y persistes el nuevo registro en la base de datos.
    new_habit = Habit(name=name)
    db.session.add(new_habit)
    db.session.commit()

    return redirect(url_for('main.index')) # rediriges al usuario a la página principal (evita reenvío del formulario)


# Completar o desmarcar hábito
@main.route('/complete/<int:habit_id>', methods=['POST']) # /<int:habit_id> captura un entero desde la URL y lo pasa a la función
def complete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id) # devuelve el objeto o dispara un 404 si no existe
    habit.completed = not habit.completed # alterna el booleano (true or false) 
    db.session.commit()
    return redirect(url_for('main.index'))


# Eliminar hábito
@main.route('/delete/<int:habit_id>', methods=['POST']) # Captura habit_id desde la URL (POST)
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id) # asegura que el hábito exista
    # marca para borrado y commit() lo ejecuta
    db.session.delete(habit) 
    db.session.commit()
    return redirect(url_for('main.index'))


# Editar hábito
@main.route('/edit/<int:habit_id>', methods=['GET', 'POST']) # permite mostrar el formulario (GET) y procesarlo (POST)
def edit_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)

    if request.method == 'POST':
        new_name = request.form.get('name') # obtiene el nuevo nombre del formulario

        # Validación: nombre vacío
        if not new_name or new_name.strip() == "":
            return "Error: El nombre no puede estar vacío.", 400 # Validas vacío
        
        # Validación: duplicado (excepto si es él mismo)
        existing = Habit.query.filter_by(name=new_name).first()
        if existing and existing.id != habit.id:
            return "Error: Ya existe un hábito con ese nombre.", 409 # valido si hay duplicado 

        habit.name = new_name # Si pasa, asignas habit.name = new_name y guardas
        db.session.commit()
        return redirect(url_for('main.index')) # Rediriges al índice

    return render_template('edit.html', habit=habit) # muestra la página con el formulario prellenado (usando habit.name en el campo)