import random
from datetime import datetime, timedelta

# Employee IDs
emp_ids = [
    'cfc71a9c-3b88-447d-a008-9cad7d104242',
    '5ce11d18-c84e-468c-9141-e71c858e5b03',
    '67086608-3277-4473-b1d2-f44cc2e2dfc8',
    '38c2d6c9-a38f-4572-8f41-c0b2745d4e4b'
]

# Function to generate random times for logs
def random_time(base_time, offset_minutes=0):
    return base_time + timedelta(minutes=random.randint(-offset_minutes, offset_minutes))

# Generate SQL insert queries for biometric logs
def generate_biometric_logs():
    print("-- Biometric Logs for March 2025")
    for emp_id in emp_ids:
        for day in range(1, 32):  # Days in March
            date = datetime(2025, 3, day)
            
            # Randomly select full day, half day, or absent
            log_type = random.choice(['full_day', 'half_day', 'absent'])
            
            if log_type == 'absent':
                continue  # No biometric log for absent days

            # Full day: 9 AM to 5 PM
            if log_type == 'full_day':
                in_time = datetime(2025, 3, day, 9, 0)
                out_time = datetime(2025, 3, day, 17, 0)
            
            # Half day: Late check-in or early checkout
            elif log_type == 'half_day':
                in_time = datetime(2025, 3, day, random.choice([11, 12]), 0)
                out_time = datetime(2025, 3, day, random.choice([13, 14]), 0)
            
            # Add small variations to simulate real data
            in_time = random_time(in_time, 15)
            out_time = random_time(out_time, 15)

            print(f"INSERT INTO biometric_logs (id, emp_id, in_time, out_time) VALUES (")
            print(f"  gen_random_uuid(), '{emp_id}', '{in_time}', '{out_time}'")
            print(");")

# Generate SQL insert queries for system logs
def generate_system_logs():
    print("\n-- System Logs for March 2025")
    for emp_id in emp_ids:
        for day in range(1, 32):  # Days in March
            date = datetime(2025, 3, day)
            
            # Randomly select full day, half day, idle time, or unexpected logout
            log_type = random.choice(['full_day', 'half_day', 'idle_time', 'unexpected_logout', 'absent'])
            
            if log_type == 'absent':
                continue  # No system log for absent days

            # Full day: 9 AM to 5:10 PM
            if log_type == 'full_day':
                start_time = datetime(2025, 3, day, 9, 0)
                end_time = datetime(2025, 3, day, 17, 10)
            
            # Half day: Late start or early end
            elif log_type == 'half_day':
                start_time = datetime(2025, 3, day, random.choice([11, 12]), 0)
                end_time = datetime(2025, 3, day, random.choice([13, 14]), 0)
            
            # Idle time: system log exceeds biometric logs (suggesting idle time)
            elif log_type == 'idle_time':
                start_time = datetime(2025, 3, day, 9, 0)
                end_time = datetime(2025, 3, day, 18, 30)
            
            # Unexpected logout: system logs after biometric logout
            elif log_type == 'unexpected_logout':
                start_time = datetime(2025, 3, day, 9, 0)
                end_time = datetime(2025, 3, day, random.choice([18, 19]), 0)

            # Add small variations to simulate real data
            start_time = random_time(start_time, 15)
            end_time = random_time(end_time, 15)
            in_ip = f"192.168.1.{random.randint(100, 150)}"
            out_ip = in_ip

            print(f"INSERT INTO system_logs (id, emp_id, start_time, end_time, in_ip_address, out_ip_address) VALUES (")
            print(f"  gen_random_uuid(), '{emp_id}', '{start_time}', '{end_time}', '{in_ip}', '{out_ip}'")
            print(");")

# Run both generators
generate_biometric_logs()
generate_system_logs()