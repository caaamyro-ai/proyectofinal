# Archivo que crea una base de datos falsa

from app import db
from app.models import DailyHabit, WeeklyHabit, WeeklyHabitCompletion
from datetime import date, timedelta
import random

def run_seed():
    print(" Generando historial falso para el año completo...")

    # 1) Obtener hábitos existentes
    weekly_habits = WeeklyHabit.query.all()
    daily_habits  = DailyHabit.query.all()

    if not weekly_habits and not daily_habits:
        print(" No existen hábitos en la base de datos.")
        print("   Crea al menos 1 hábito antes de ejecutar este seed.")
        return

    # 2) Fechas del año
    start = date(2024, 11, 21)
    end   = date(2025, 11, 21)
    current = start

    # 3) Simulación día por día
    while current <= end:

        # --- SEMANALES ---
        for habit in weekly_habits:
            if random.random() < 0.55:  # 55%
                entry = WeeklyHabitCompletion(
                    weekly_habit_id=habit.id,  # válido
                    date=current,
                    completed=True
                )
                db.session.add(entry)

        # --- DIARIOS ---
        for habit in daily_habits:
            if random.random() < 0.65:  # 65%
                entry = WeeklyHabitCompletion(
                    weekly_habit_id=None,   # ahora es válido
                    date=current,
                    completed=True
                )
                db.session.add(entry)

        current += timedelta(days=1)

    db.session.commit()

    print(" Historial generado con éxito.")
