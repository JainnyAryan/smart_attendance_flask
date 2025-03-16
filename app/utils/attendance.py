from datetime import datetime, timedelta


def determine_attendance_status(in_time, out_time, shift_start, shift_end, full_day_hours, half_day_hours):
    if not in_time or not out_time:
        return "Absent"

    # Convert to datetime objects
    in_time = datetime.strptime(str(in_time), "%Y-%m-%d %H:%M:%S")
    out_time = datetime.strptime(str(out_time), "%Y-%m-%d %H:%M:%S")

    shift_start = datetime.strptime(str(shift_start), "%H:%M:%S").time()
    shift_end = datetime.strptime(str(shift_end), "%H:%M:%S").time()

    # Calculate work duration
    work_duration = (out_time - in_time).total_seconds() / 3600

    # Determine attendance status
    if work_duration >= float(full_day_hours):
        return "Full Day"
    elif work_duration >= float(half_day_hours):
        return "Half Day"
    else:
        return "Absent"
