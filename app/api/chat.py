import os
from dotenv import load_dotenv
import requests
from fastapi import APIRouter, Depends
from app.api.performance import get_allocation_score_breakdown, get_employee_performance_score
from app.auth.auth import get_current_user
from app.crud.chat import *
from app.database import get_db
from app.models.user import User
from app.schemas.biometric_log import BiometricLogResponse
from app.schemas.chat import ChatResponse, ChatRequest
from app.schemas.project import ProjectResponse
from app.schemas.employee import EmployeeResponse
from app.schemas.project_allocation import ProjectAllocationResponse
from app.schemas.system_log import SystemLogResponse


router = APIRouter()

load_dotenv()
CHATBOT_SERVICE_URL = os.getenv("CHATBOT_BASE_URL")


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db=Depends(get_db), user: User = Depends(get_current_user)):
    response = requests.post(f"{CHATBOT_SERVICE_URL}/process_chat", json={
                             "message": request.message})
    chatbot_data = response.json()

    msg_response: str = chatbot_data["response"]
    intent = chatbot_data["intent"]
    confidence = chatbot_data["confidence"]
    entities = chatbot_data["entities"]
    category = chatbot_data["category"]

    if confidence < 0.3 and confidence > 0:
        return {"response": "Sorry, I didn\'t understand that.",  "confidence": confidence, "intent": intent, "data": None}

    # =================GREETINGS=================
    if category == "greetings":
        name = get_my_name(user=user)
        response_msg = msg_response.format(name)
        return {"response": response_msg, "confidence": confidence, "intent": intent, "data": None}

    # =================EMPLOYEE INTENTS=================
    if category == "employee_intents" and user.is_admin:
        return {"response": "You're not authorized to access this information.", "confidence": confidence, "intent": intent, "data": None}
    match intent:
        case "my_attendance_check":
            response_msg = msg_response
            attd_data = None
            attd_data = get_my_employee_today_attendance_data(db, user)
            if not attd_data:
                return {"response": "Couldn't fetch attendance data. Please try again later...", "confidence": confidence, "intent": intent, "data": None}
            biometric_logs = [BiometricLogResponse.model_validate(
                b).model_dump() for b in attd_data["biometric_logs"]]
            system_logs = [SystemLogResponse.model_validate(
                s).model_dump() for s in attd_data["system_logs"]]
            return {"response": response_msg, "confidence": confidence, "intent": intent, "data": {"biometric_logs": biometric_logs, "system_logs": system_logs}}

        case "my_project_allocations":
            response_msg = msg_response
            alloc_data = None
            alloc_data = get_my_project_allocations(db=db, user=user)
            if not alloc_data:
                return {"response": "Couldn't fetch project allocations. Please try again later...", "confidence": confidence, "intent": intent, "data": None}
            alloc_data = [ProjectAllocationResponse.model_validate(
                a).model_dump() for a in alloc_data]
            return {"response": response_msg, "confidence": confidence, "intent": intent, "data": {"project_allocations": alloc_data}}

        case "my_current_score":
            response_msg = msg_response
            score_data = None
            score_data = get_employee_performance_score(
                db=db, employee_id=user.employee[0].id)
            if not score_data:
                return {"response": "Couldn't fetch performance score. Please try again later...", "confidence": confidence, "intent": intent, "data": None}
            return {"response": response_msg, "confidence": confidence, "intent": intent, "data": {"score": score_data}}

        case "my_score_breakdown":
            response_msg = msg_response
            breakdown_data = None
            breakdown_data = get_allocation_score_breakdown(
                db=db, employee_id=user.employee[0].id)
            if not breakdown_data:
                return {"response": "Couldn't fetch performance score breakdown. Please try again later...", "confidence": confidence, "intent": intent, "data": None}
            return {"response": response_msg, "confidence": confidence, "intent": intent, "data": {"breakdown_data": breakdown_data}}

    # =================ADMIN INTENTS=================
    if category == "admin_intents" and not user.is_admin:
        return {"response": "You're not authorized to access this information.", "confidence": confidence, "intent": intent, "data": None}
    match intent:
        case "employee_details":
            response_msg = msg_response
            emp_data = None
            if not entities:
                return {"response": "Please try entering exact full name of the employee...", "confidence": confidence, "intent": intent, "data": None}
            for ent in entities:
                if ent["label"] == "EMPLOYEE_NAME":
                    emp_data = get_employee_details(db=db, query=ent['name'])
                    if emp_data:
                        response_msg = msg_response.format(ent["name"])
                        break
            if not emp_data:
                return {"response": "Couldn't fetch employee information. Please try entering exact full name...", "confidence": confidence, "intent": intent, "data": None}
            emp_data = EmployeeResponse.model_validate(emp_data).model_dump()
            return {"response": response_msg, "confidence": confidence, "intent": intent, "data": {"employee": emp_data}}

        case "employee_attendance_summary":
            response_msg = msg_response
            attd_data = None
            if not entities:
                return {"response": "Please try entering exact full name of the employee...", "confidence": confidence, "intent": intent, "data": None}
            for ent in entities:
                if ent["label"] == "EMPLOYEE_NAME":
                    attd_data = get_attendance_stats(db=db, name=ent['name'])
                    if attd_data:
                        response_msg = msg_response.format(ent["name"])
                        break
            if not attd_data:
                return {"response": "Couldn't fetch attendance data. Please try entering exact full name...", "confidence": confidence, "intent": intent, "data": None}
            return {"response": response_msg, "confidence": confidence, "intent": intent, "data": attd_data}

        case "all_projects":
            response_msg = msg_response
            projects_data = get_all_projects(db=db)
            if not projects_data:
                return {"response": "Couldn't fetch ongoing projects data.", "confidence": confidence, "intent": intent, "data": None}
            projects_data = [ProjectResponse.model_validate(
                p).model_dump() for p in projects_data]
            return {"response": response_msg, "confidence": confidence, "intent": intent, "data": {"projects": projects_data}}

        case "project_details":
            response_msg = msg_response
            project_data = None
            if not entities:
                return {"response": "Please try entering exact project code...", "confidence": confidence, "intent": intent, "data": None}
            for ent in entities:
                if ent["label"] == "PROJECT_CODE":
                    project_data = get_project_details(
                        db=db, code=ent['name'])
                    if project_data:
                        response_msg = msg_response.format(ent["name"])
                        break
            if not project_data:
                return {"response": "Couldn't fetch project details. Please try entering exact project code...", "confidence": confidence, "intent": intent, "data": None}
            project_data = ProjectResponse.model_validate(
                project_data).model_dump()
            return {"response": response_msg, "confidence": confidence, "intent": intent, "data": {"project": project_data}}

        case "current_allocations_of_project":
            response_msg = msg_response
            alloc_data = None
            if not entities:
                return {"response": "Please try entering exact project code...", "confidence": confidence, "intent": intent, "data": None}
            for ent in entities:
                if ent["label"] == "PROJECT_CODE":
                    alloc_data = get_project_allocations_of_project(
                        db=db, code=ent['name'])
                    if alloc_data:
                        response_msg = msg_response.format(ent["name"])
                        break
            if not alloc_data:
                return {"response": "Couldn't fetch project allocations. Please try entering exact project code...", "confidence": confidence, "intent": intent, "data": None}
            alloc_data = [ProjectAllocationResponse.model_validate(
                a).model_dump() for a in alloc_data]
            return {"response": response_msg, "confidence": confidence, "intent": intent, "data": {"project_allocations": alloc_data}}

        case "project_allocation_suggestions":
            response_msg = msg_response
            alloc_data = None
            if not entities:
                return {"response": "Please try entering exact project code...", "confidence": confidence, "intent": intent, "data": None}
            for ent in entities:
                if ent["label"] == "PROJECT_CODE":
                    alloc_data = get_suggested_employees_for_project(
                        db=db, code=ent['name'])
                    if alloc_data:
                        response_msg = msg_response.format(ent["name"])
                        break
            if not alloc_data:
                return {"response": "Couldn't fetch suggestions. Please try entering exact project code...", "confidence": confidence, "intent": intent, "data": None}
            alloc_data = [EmployeeResponse.model_validate(
                e).model_dump() for e in alloc_data]
            return {"response": response_msg, "confidence": confidence, "intent": intent, "data": {"allocation_suggestions": alloc_data}}

    return {"response": "I'm still learning! I'll improve over time.",  "confidence": confidence, "intent": intent, "data": None}
