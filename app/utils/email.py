from sqlalchemy.orm import Session
from app.models.employee import Employee
import re

ORG_DOMAIN = "myorg.com"

def generate_unique_email(db: Session, name: str):
    base_email = re.sub(r'\s+', '.', name.lower())
    email = f"{base_email}@{ORG_DOMAIN}"
    counter = 1

    while db.query(Employee).filter(Employee.email == email).first():
        email = f"{base_email}{counter}@{ORG_DOMAIN}"
        counter += 1

    return email