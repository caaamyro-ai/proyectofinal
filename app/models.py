#Este archivo define una tabla para el tracker 

# Importa la base de datos ya creada en __init__.py
from . import db  

# Define una clase llamada Habit, que representa una tabla en la base de datos
class Habit(db.Model): # define una clase llamada Habit, que representa una tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # name será una cadena de texto con un máximo de 100 caracteres
    completed = db.Column(db.Boolean, default=False) #completed será un valor booleano, y default false hace que 
    # al crear un nuevo hábito, por defecto esté no completado
    # id será una columna entera (Integer).
    # primary_key=True significa que este campo será el identificador único de cada registro 
    # nullable = false indica que no puede quedar vacío (es obligatorio)