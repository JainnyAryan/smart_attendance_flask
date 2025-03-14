import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")
engine = create_engine(DATABASE_URL)

# Function to generate random times
def random_time(base_time, offset_minutes=0):
    """Add a random time offset (±offset_minutes) to a base time."""
    return (datetime.combine(datetime.today(), base_time) + timedelta(minutes=random.randint(-offset_minutes, offset_minutes))).time()

# Get employee shift details using raw SQL
def get_shift_details():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT e.id AS emp_id, s.start_time, s.end_time 
            FROM employees e
            JOIN shifts s ON e.shift_id = s.id
        """))
        return result.fetchall()

# Generate biometric and system logs
def generate_logs(month, year):
    employees = get_shift_details()
    
    print("-- Generating Biometric and System Logs")

    with engine.connect() as conn:
        trans = conn.begin()
        try:
            for emp_id, start_time, end_time in employees:
                for day in range(1, 32):
                    try:
                        date = datetime(year, month, day)
                    except ValueError:
                        break  # Skip invalid days like Feb 30

                    log_type = random.choice(['full_day', 'half_day', 'absent'])
                    if log_type == 'absent':
                        continue

                    # Generate biometric log times
                    if log_type == 'full_day':
                        bio_in_time = random_time(start_time, 15)
                        bio_out_time = random_time(end_time, 15)
                    elif log_type == 'half_day':
                        bio_in_time = random_time(start_time, 60)
                        bio_out_time = random_time(start_time, 120)

                    bio_in_datetime = datetime.combine(date, bio_in_time)
                    bio_out_datetime = datetime.combine(date, bio_out_time)

                    if bio_in_datetime >= bio_out_datetime:
                        continue  # Skip invalid time entries

                    # System log: sometimes different, sometimes same as biometric
                    if random.choice([True, False]):
                        sys_in_time = bio_in_datetime + timedelta(minutes=random.randint(1, 10))
                        sys_out_time = bio_out_datetime - timedelta(minutes=random.randint(1, 10))

                        # Ensure system logs are within biometric logs
                        if sys_in_time >= sys_out_time:
                            sys_in_time, sys_out_time = bio_in_datetime, bio_out_datetime
                    else:  
                        sys_in_time = bio_in_datetime
                        sys_out_time = bio_out_datetime

                    # Ensure system log duration is less than biometric log duration
                    if sys_in_time < bio_in_datetime:
                        sys_in_time = bio_in_datetime
                    if sys_out_time > bio_out_datetime:
                        sys_out_time = bio_out_datetime
                    if sys_in_time >= sys_out_time:
                        continue  # Skip invalid time entries

                    # Insert biometric logs
                    conn.execute(text("""
                        INSERT INTO biometric_logs (id, emp_id, in_time, out_time)
                        VALUES (gen_random_uuid(), :emp_id, :in_time, :out_time)
                    """), {
                        "emp_id": emp_id,
                        "in_time": bio_in_datetime,
                        "out_time": bio_out_datetime
                    })

                    # Insert system logs with randomized IPs
                    in_ip = f"192.168.1.{random.randint(100, 150)}"
                    out_ip = in_ip

                    conn.execute(text("""
                        INSERT INTO system_logs (id, emp_id, start_time, end_time, in_ip_address, out_ip_address)
                        VALUES (gen_random_uuid(), :emp_id, :start_time, :end_time, :in_ip, :out_ip)
                    """), {
                        "emp_id": emp_id,
                        "start_time": sys_in_time,
                        "end_time": sys_out_time,
                        "in_ip": in_ip,
                        "out_ip": out_ip
                    })

            trans.commit()
            print("✅ Logs generated and inserted successfully.")
        except Exception as e:
            trans.rollback()
            print("❌ Error inserting logs:", e)

# Let user pick month and year
def main():
    try:
        month = int(input("Enter the month (1-12): "))
        year = int(input("Enter the year (e.g., 2025): "))
        generate_logs(month, year)
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()