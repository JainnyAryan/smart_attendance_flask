import os
from dotenv import load_dotenv
import requests
from fastapi import APIRouter, Depends
from app.crud.chat import get_attendance_stats
from app.database import get_db
from app.schemas.chat import ChatResponse, ChatRequest


router = APIRouter()

load_dotenv()
CHATBOT_SERVICE_URL = os.getenv("CHATBOT_BASE_URL")


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db=Depends(get_db)):
    response = requests.post(f"{CHATBOT_SERVICE_URL}/process_chat", json={
                             "message": request.message})
    chatbot_data = response.json()

    msg_response: str = chatbot_data["response"]
    intent = chatbot_data["intent"]
    confidence = chatbot_data["confidence"]
    entities = chatbot_data["entities"]
    category = chatbot_data["category"]

    if confidence < 0.3:
        return {"response": "Sorry, I didn\'t understand that.",  "confidence": confidence, "intent": intent, "data": None}

    if category == "greetings":
        return {"response": msg_response, "confidence": confidence, "intent": intent, "data": None}
    if intent == "employee_attendance_summary":
        response_msg = msg_response
        attd_data = None
        if len(entities) == 0:
            return {"response": "Please try entering exact full name of the employee...", "confidence": confidence, "intent": intent, "data": None}
        for ent in entities:
            if ent["label"] == "PERSON":
                attd_data = get_attendance_stats(db=db, name=ent['name'])
                if not attd_data:
                    continue
                response_msg = msg_response.format(ent["name"])
                break
        
        if not attd_data:
            return {"response": f"Couldn't fetch attendance data. Please try entering exact full name...", "confidence": confidence, "intent": intent, "data": None}

        return {"response": response_msg, "confidence": confidence, "intent": intent, "data": attd_data}

    return {"response": "I'm still learning! I'll improve over time.",  "confidence": confidence, "intent": intent, "data": None}
