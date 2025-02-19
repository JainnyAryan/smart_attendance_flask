import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api import employee, auth, admin, user, me
from app.database import engine, Base
from app.models import employee, department, designation, shift, biometric_log, system_log
from app.api import employee as employee_api

log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

uvicorn_log_config = uvicorn.config.LOGGING_CONFIG
uvicorn_log_config["formatters"]["default"]["fmt"] = log_format

logger = logging.getLogger("uvicorn")


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
app.include_router(employee_api.router, prefix="/api/employee")
app.include_router(auth.router, prefix="/api")
app.include_router(admin.router, prefix="/api/admin")
app.include_router(user.router, prefix="/api")
app.include_router(me.router, prefix="/api")

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Attendance Monitoring System"}