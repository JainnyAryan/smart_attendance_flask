from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.attendance import determine_attendance_status


def get_attendance_calendar_data(
    emp_id: str,
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):
    try:
        # Convert string dates to datetime.date
        parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # SQL Query to fetch biometric logs and shifts
        query = text("""
            SELECT 
                b.in_time,
                b.out_time,
                b.in_time::date AS log_date,
                s.start_time,
                s.end_time,
                s.total_hours,
                s.half_day_shift_hours
            FROM biometric_logs b
            LEFT JOIN employees e ON b.emp_id = e.id
            LEFT JOIN shifts s ON e.shift_id = s.id
            WHERE b.emp_id = :emp_id
              AND b.in_time::date BETWEEN :start_date AND :end_date
            ORDER BY log_date;
        """)

        # Execute query and get results with key-based access
        results = db.execute(query, {
            "emp_id": emp_id,
            "start_date": start_date,
            "end_date": end_date
        }).mappings().all()  # <-- Converts rows to key-value dicts

        # Prepare attendance data
        calendar_data = {}

        # Calculate attendance status for each result
        for result in results:
            log_date = result["log_date"]
            status = determine_attendance_status(
                result["in_time"],
                result["out_time"],
                result["start_time"],
                result["end_time"],
                result["total_hours"],
                result["half_day_shift_hours"]
            )

            # Handle night shift correctly by adding status for the next day if applicable
            if result["end_time"] < result["start_time"]:
                next_day = log_date + timedelta(days=1)
                calendar_data[next_day] = status

            calendar_data[log_date] = status

        # Ensure all dates are covered
        current_date = parsed_start_date
        while current_date <= parsed_end_date:
            if current_date not in calendar_data:
                calendar_data[current_date] = "Absent"
            current_date += timedelta(days=1)

        # Format for frontend
        formatted_calendar = [
            {"date": str(date), "status": status}
            for date, status in sorted(calendar_data.items())
        ]

        return {"employee_id": emp_id, "calendar": formatted_calendar}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))