#ESTE ARCHIVO CONTIENE DATOS FALSOS PARA QUE VEAMOS ESTADÍSTICAS 

from app import db
from app.models import DailyHabit, WeeklyHabit

def seed_data():
    print("Creando hábitos de ejemplo...")

    h1 = DailyHabit(name="Tomar agua")
    h2 = DailyHabit(name="Caminar 20 minutos")

    h3 = WeeklyHabit(name="Ir al gimnasio", days="mon,wed,fri")
    h4 = WeeklyHabit(name="Estudiar 2 horas", days="tue,thu")

    db.session.add_all([h1, h2, h3, h4])
    db.session.commit()

    print("Datos insertados correctamente.")
