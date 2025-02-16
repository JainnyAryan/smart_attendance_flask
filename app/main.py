from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import employee, attendance, auth, admin  # Use absolute imports
from app.database import engine, Base
from app.models import employee, department, designation, shift, biometric_log
from app.api import employee as employee_api

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Include Routers
app.include_router(employee_api.router, prefix="/api")
app.include_router(attendance.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(admin.router, prefix="/api/admin")

@app.get("/")
def read_root():
    return {"message": "Attendance Monitoring System"}