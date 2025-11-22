# Archivo que crea una base de datos falsa

from app import create_app, db
from app.models import DailyHabit, WeeklyHabit, WeeklyHabitCompletion
from datetime import date, timedelta
import random

def run_seed():
    print("🌱 Generando historial falso para el año completo...")

    # 1) Obtener hábitos existentes
    weekly_habits = WeeklyHabit.query.all()
    daily_habits  = DailyHabit.query.all()

    if not weekly_habits and not daily_habits:
        print("⚠️  No existen hábitos en la base de datos.")
        print("   Crea al menos 1 hábito antes de ejecutar este seed.")
        return

    # 2) Fechas del año (último año completo)
    start = date(2024, 11, 21)
    end   = date(2025, 11, 21)
    current = start

    total_entries = 0

    # 3) Simulación día por día
    while current <= end:

        # --- HÁBITOS SEMANALES ---
        for habit in weekly_habits:
            if random.random() < 0.55:  # 55% de probabilidad
                entry = WeeklyHabitCompletion(
                    habit_id=habit.id,        # NUEVO
                    habit_type="weekly",      # NUEVO
                    date=current,
                    completed=True
                )
                db.session.add(entry)
                total_entries += 1

        # --- HÁBITOS DIARIOS ---
        for habit in daily_habits:
            if random.random() < 0.65:  # 65% de probabilidad
                entry = WeeklyHabitCompletion(
                    habit_id=habit.id,        # NUEVO
                    habit_type="daily",       # NUEVO
                    date=current,
                    completed=True
                )
                db.session.add(entry)
                total_entries += 1

        current += timedelta(days=1)

    db.session.commit()

    print(f"✅ Historial generado con éxito.")
    print(f"📊 Total de registros creados: {total_entries}")
    print(f"📅 Período: {start} a {end}")
    print(f"   - Hábitos semanales: {len(weekly_habits)}")
    print(f"   - Hábitos diarios: {len(daily_habits)}")

# Para ejecutar directamente
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        run_seed()