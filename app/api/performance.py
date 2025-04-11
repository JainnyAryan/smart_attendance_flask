from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.auth import get_current_admin, get_current_user
from app.database import get_db
from app.models.project_allocation import ProjectAllocation
from app.models.project_allocation_status_log import ProjectAllocationStatusLog
from collections import defaultdict
from datetime import datetime

from app.models.user import User
from app.utils.performance import compute_allocation_metrics, group_status_logs_by_allocation, score_allocation

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/employee/{employee_id}/performance-score", response_model=float)
def get_employee_performance_score(employee_id: UUID, db: Session = Depends(get_db)):
    logs = db.query(ProjectAllocationStatusLog).join(ProjectAllocation).filter(ProjectAllocation.employee_id == employee_id).all()
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found for this employee")

    grouped_logs = group_status_logs_by_allocation(logs)
    total_score, count = 0, 0

    for allocation_id, log_list in grouped_logs.items():
        alloc = db.query(ProjectAllocation).filter_by(id=allocation_id).first()
        if not alloc:
            continue
        metrics = compute_allocation_metrics(log_list, alloc.deadline)
        score = score_allocation(metrics)
        total_score += score
        count += 1

    return round(total_score / count, 2) if count > 0 else 0


@router.get("/employee/{employee_id}/allocation-performance-breakdown")
def get_allocation_score_breakdown(employee_id: UUID, db: Session = Depends(get_db)):
    logs = db.query(ProjectAllocationStatusLog).join(ProjectAllocation).filter(ProjectAllocation.employee_id == employee_id).all()
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found for this employee")

    grouped_logs = group_status_logs_by_allocation(logs)

    breakdown = []
    for allocation_id, log_list in grouped_logs.items():
        alloc = db.query(ProjectAllocation).filter_by(id=allocation_id).first()
        if not alloc:
            continue
        metrics = compute_allocation_metrics(log_list, alloc.deadline)
        score = score_allocation(metrics)
        breakdown.append({
            "allocation_id": str(allocation_id),
            "project": {
                "name": alloc.project.name,
                "code": alloc.project.code
            },
            "score": score,
            "metrics": metrics
        })

    return breakdown

#--------------FOR ADMINS-----------------
@router.get("/admin/employee-performance-scores")
def get_all_employee_scores(db: Session = Depends(get_db), user: User = Depends(get_current_admin)):
    from app.models.employee import Employee
    employees = db.query(Employee).all()
    scores = []

    for emp in employees:
        logs = db.query(ProjectAllocationStatusLog).join(ProjectAllocation).filter(ProjectAllocation.employee_id == emp.id).all()
        if not logs:
            continue

        grouped_logs = group_status_logs_by_allocation(logs)
        total_score, count = 0, 0

        for allocation_id, log_list in grouped_logs.items():
            alloc = db.query(ProjectAllocation).filter_by(id=allocation_id).first()
            if not alloc:
                continue
            metrics = compute_allocation_metrics(log_list, alloc.deadline)
            score = score_allocation(metrics)
            total_score += score
            count += 1

        if count > 0:
            scores.append({
                "employee_id": str(emp.id),
                "name": emp.name,
                "emp_code": emp.emp_code,
                "score": round(total_score / count, 2)
            })

    return scores
