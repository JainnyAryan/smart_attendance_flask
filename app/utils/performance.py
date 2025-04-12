from collections import defaultdict


def group_status_logs_by_allocation(logs):
    grouped = defaultdict(list)
    for log in logs:
        grouped[log.allocation_id].append(log)
    for logs in grouped.values():
        logs.sort(key=lambda x: x.changed_at)
    return grouped


def compute_allocation_metrics(logs, deadline):
    total_time = 0
    active_time = 0
    hold_time = 0
    completed_time = None
    transition_counts = 0

    for log in logs:
        if log.duration_spent:
            seconds = log.duration_spent.total_seconds()
            total_time += seconds
            if log.from_status.name == "ACTIVE":
                active_time += seconds
            elif log.from_status.name == "ON_HOLD":
                hold_time += seconds

        transition_counts += 1

        if log.to_status.name == "COMPLETED":
            completed_time = log.changed_at

    return {
        "total_time": total_time,
        "active_time": active_time,
        "hold_time": hold_time,
        "transitions": transition_counts,
        "completed_on_time": completed_time is not None and completed_time.date() <= deadline
    }


def score_allocation(metrics):
    if metrics["total_time"] == 0:
        return 0

    active_ratio = metrics["active_time"] / metrics["total_time"]
    hold_ratio = metrics["hold_time"] / metrics["total_time"]
    transition_penalty = min(metrics["transitions"] / 10, 1.0)

    score = (
        0.5 * active_ratio +
        0.2 * int(metrics["completed_on_time"]) +
        0.2 * (1 - hold_ratio) -
        0.1 * transition_penalty
    )
    return round(score * 100, 2)
