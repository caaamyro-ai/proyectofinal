#ESTE ARCHIVO CONTIENE DATOS FALSOS PARA QUE VEAMOS ESTADÍSTICAS 


from app import app, db
from app.models import DailyHabit, WeeklyHabit, WeeklyHabitCompletion
from datetime import date, timedelta

with app.app_context():

    print("⚙️ Creando datos de prueba...")

    # 1) Hábitos diarios
    
    h1 = DailyHabit(name="Tomar agua")
    h2 = DailyHabit(name="Hacer estiramientos")

    db.session.add_all([h1, h2])
    db.session.commit()


    # 2) Hábitos semanales

    w1 = WeeklyHabit(
        name="Ir al gimnasio",
        days="mon,wed,fri"
    )

    w2 = WeeklyHabit(
        name="Estudiar Python",
        days="tue,thu"
    )

    db.session.add_all([w1, w2])
    db.session.commit()


    # 3) Registros semanales (últimos 5 días)

    for i in range(5):
        db.session.add(
            WeeklyHabitCompletion(
                weekly_habit_id=w1.id,
                date=date.today() - timedelta(days=i),
                completed=True
            )
        )

    db.session.commit()

    print("✨ Datos cargados exitosamente")
