from sqlalchemy.orm import Session
from sqlalchemy import Date, cast
from app.models.biometric_log import BiometricLog
from app.models.system_log import SystemLog
from datetime import datetime, timedelta


def calculate_time_wastage(db: Session, emp_id: str, start_date: str, end_date: str):
    # Convert string dates to datetime objects
    parsed_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    parsed_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    print("Start Date:", parsed_start_date)
    print("End Date:", parsed_end_date)

    # Query biometric logs
    bio_logs = db.query(BiometricLog).filter(
        BiometricLog.emp_id == emp_id,
        cast(BiometricLog.in_time, Date) >= parsed_start_date,
        cast(BiometricLog.out_time, Date) <= parsed_end_date
    ).all()

    # Query system logs
    sys_logs = db.query(SystemLog).filter(
        SystemLog.emp_id == emp_id,
        cast(SystemLog.start_time, Date) >= parsed_start_date,
        cast(SystemLog.end_time, Date) <= parsed_end_date
    ).all()

    # Group biometric logs by date
    bio_logs_by_date = {}
    for bio in bio_logs:
        date = bio.in_time.date()
        bio_logs_by_date[date] = bio_logs_by_date.get(
            date, timedelta()) + (bio.out_time - bio.in_time)

    # Group system logs by date
    sys_logs_by_date = {}
    for sys in sys_logs:
        date = sys.start_time.date()
        sys_logs_by_date[date] = sys_logs_by_date.get(
            date, timedelta()) + (sys.end_time - sys.start_time)

    # Calculate time wastage
    time_wastage_data = []
    all_dates = set(bio_logs_by_date.keys()).union(
        set(sys_logs_by_date.keys()))

    for date in all_dates:
        bio_duration = bio_logs_by_date.get(date, timedelta())
        sys_duration = sys_logs_by_date.get(date, timedelta())
        wasted_time = bio_duration - sys_duration

        time_wastage_data.append({
            "date": date,
            "bio_duration": bio_duration.total_seconds(),
            "sys_duration": sys_duration.total_seconds(),
            "wasted_time": wasted_time.total_seconds(),
        })

    # Sort data by date (earliest to latest)
    sorted_time_wastage_data = sorted(
        time_wastage_data, key=lambda x: x['date'])

    return sorted_time_wastage_data
