import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")
engine = create_engine(DATABASE_URL)

def generate_designations():
    designations = [
        ("ENGR", "Engineer"),
        ("MGR", "Manager"),
        ("DIR", "Director"),
        ("ANL", "Analyst"),
        ("EXEC", "Executive"),
        ("DEV", "Developer"),
    ]

    with engine.connect() as conn:
        trans = conn.begin()
        try:
            for designation_code, name in designations:
                conn.execute(text("""
                    INSERT INTO designations (id, designation_code, name)
                    VALUES (gen_random_uuid(), :designation_code, :name)
                """), {"designation_code": designation_code, "name": name})
            
            trans.commit()
            print("✅ Designations inserted successfully.")
        except Exception as e:
            trans.rollback()
            print("❌ Error inserting designations:", e)

if __name__ == "__main__":
    generate_designations()