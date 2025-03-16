import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")
engine = create_engine(DATABASE_URL)

def generate_departments():
    departments = [
        ("HR", "Human Resources"),
        ("ENG", "Engineering"),
        ("FIN", "Finance"),
        ("MKT", "Marketing"),
        ("SALES", "Sales"),
        ("IT", "Information Technology"),
    ]

    with engine.connect() as conn:
        trans = conn.begin()
        try:
            for dept_code, name in departments:
                conn.execute(text("""
                    INSERT INTO departments (id, dept_code, name)
                    VALUES (gen_random_uuid(), :dept_code, :name)
                """), {"dept_code": dept_code, "name": name})
            
            trans.commit()
            print("✅ Departments inserted successfully.")
        except Exception as e:
            trans.rollback()
            print("❌ Error inserting departments:", e)

if __name__ == "__main__":
    generate_departments()