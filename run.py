from app import create_app

app = create_app()

if __name__ == '__main__': # Ejecuta el siguiente bloque solo si este archivo se está ejecutando directamente, no si fue importado desde otro.
    # Inicia el servidor web local y corre la aplicación
    app.run(debug=True) 