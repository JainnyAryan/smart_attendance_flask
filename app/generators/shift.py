import os
import random
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")
engine = create_engine(DATABASE_URL)

def generate_shifts():
    shifts = [
        ("MORNING", "Morning Shift", "09:00:00", "17:00:00", 1.00, 8.00, 4.00, 15, 15, 1),
        ("EVENING", "Evening Shift", "14:00:00", "22:00:00", 1.00, 8.00, 4.00, 10, 10, 1),
        ("NIGHT", "Night Shift", "22:00:00", "06:00:00", 1.00, 8.00, 4.00, 5, 5, 0),
    ]

    with engine.connect() as conn:
        trans = conn.begin()
        try:
            for shift in shifts:
                conn.execute(text("""
                    INSERT INTO shifts (id, shift_code, name, start_time, end_time, break_time, total_hours, 
                                       half_day_shift_hours, late_coming_mins, early_going_mins, same_day)
                    VALUES (gen_random_uuid(), :shift_code, :name, :start_time, :end_time, :break_time, :total_hours, 
                            :half_day_shift_hours, :late_coming_mins, :early_going_mins, :same_day)
                """), dict(zip(["shift_code", "name", "start_time", "end_time", "break_time", "total_hours",
                                "half_day_shift_hours", "late_coming_mins", "early_going_mins", "same_day"], shift)))
            
            trans.commit()
            print("✅ Shifts inserted successfully.")
        except Exception as e:
            trans.rollback()
            print("❌ Error inserting shifts:", e)

if __name__ == "__main__":
    generate_shifts()