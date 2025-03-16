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
            SELECT e.id AS emp_id, e.name AS emp_name, s.start_time, s.end_time 
            FROM employees e
            JOIN shifts s ON e.shift_id = s.id
        """))
        return result.fetchall()

# Generate biometric and system logs
def generate_logs(month, year):
    employees = get_shift_details()

    print("-- Generating Biometric and System Logs")

    # Adjusted probability distribution for attendance
    log_choices = (['full_day']) * 10 + (['half_day'] * 3) + (['absent'] * 2)

    total_bio_logs = 0
    total_sys_logs = 0
    employee_log_counts = {}

    with engine.connect() as conn:
        trans = conn.begin()
        try:
            for emp_id, emp_name, start_time, end_time in employees:
                emp_bio_logs = 0
                emp_sys_logs = 0

                for day in range(1, 32):
                    try:
                        date = datetime(year, month, day)
                    except ValueError:
                        break  # Skip invalid days like Feb 30

                    log_type = random.choice(log_choices)  # Pick based on adjusted probabilities
                    if log_type == 'absent':
                        continue  # Skip to the next day

                    # Generate biometric log times
                    if log_type == 'full_day':
                        bio_in_time = random_time(start_time, 40)
                        bio_out_time = random_time(end_time, 40)
                    elif log_type == 'half_day':
                        bio_in_time = random_time(start_time, 120)
                        bio_out_time = random_time(end_time, 150)

                    bio_in_datetime = datetime.combine(date, bio_in_time)

                    # Handling night shifts (end_time < start_time means shift ends next day)
                    if end_time < start_time:
                        bio_out_datetime = datetime.combine(date + timedelta(days=1), bio_out_time)
                    else:
                        bio_out_datetime = datetime.combine(date, bio_out_time)

                    if bio_in_datetime >= bio_out_datetime:
                        continue  # Skip invalid time entries

                    # Generate system log ensuring constraints
                    sys_in_time = bio_in_datetime + timedelta(minutes=random.randint(1, 10))  # Always after biometric in
                    sys_out_time = bio_out_datetime - timedelta(minutes=random.randint(1, 10))  # Always before biometric out

                    # Ensure system log duration is less than biometric log duration
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
                    emp_bio_logs += 1
                    total_bio_logs += 1

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
                    emp_sys_logs += 1
                    total_sys_logs += 1

                # Store log count for each employee
                employee_log_counts[f"{emp_id} - {emp_name}"] = {
                    "biometric_logs": emp_bio_logs,
                    "system_logs": emp_sys_logs
                }

            trans.commit()
            print("✅ Logs generated and inserted successfully.\n")

            # Print employee-wise log counts
            print("-- Logs Generated Per Employee --")
            for emp_id, counts in employee_log_counts.items():
                print(f"Employee ID - Name: {emp_id} -> Biometric Logs: {counts['biometric_logs']}, System Logs: {counts['system_logs']}")

            # Print total log counts
            print("\n-- Total Logs Generated --")
            print(f"Total Biometric Logs: {total_bio_logs}")
            print(f"Total System Logs: {total_sys_logs}")

        except Exception as e:
            trans.rollback()
            print("❌ Error inserting logs:", e)

# Let user pick month and year
def main():
    try:
        month = int(input("Enter the month (1-12): "))
        if month not in range(1, 13):
            raise ValueError("Month should be between 1 and 12.")
        year = int(input("Enter the year (e.g., 2025): "))
        if year < 2000 or year > 2100:
            raise ValueError("Year should be between 2000 and 2100.")
        generate_logs(month, year)
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()