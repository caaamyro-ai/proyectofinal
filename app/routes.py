from flask import Blueprint, render_template

# Definir un "blueprint" para las rutas principales
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

