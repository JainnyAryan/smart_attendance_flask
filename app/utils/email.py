from datetime import datetime
import random
from sqlalchemy.orm import Session
from app.models.employee import Employee
import re
import os
import resend
from dotenv import load_dotenv

# ORG_DOMAIN = "myorg.com"
ORG_DOMAIN = "resend.dev"
load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")


def generate_unique_email(db: Session, name: str):
    base_email = re.sub(r'\s+', '.', name.lower())
    email = f"{base_email}@{ORG_DOMAIN}"
    counter = 1

    while db.query(Employee).filter(Employee.email == email).first():
        email = f"{base_email}{counter}@{ORG_DOMAIN}"
        counter += 1

    return email


def generate_emp_code(db: Session, name: str) -> str:
    joining_year = datetime.now().year
    year_part = str(joining_year)[-2:]
    name_parts = name.split()
    initials = ''.join([part[0] for part in name_parts[:3]]).upper().ljust(
        3, name_parts[-1][1].upper())

    serial_number = 1

    while True:
        serial_part = f"{serial_number:04d}"  # Ensure 3-digit serial number
        emp_code = f"{year_part}{initials}{serial_part}"

        existing_emp = db.query(Employee).filter(
            Employee.emp_code == emp_code).first()
        if not existing_emp:
            return emp_code 

        shuffled_initials = ''.join(random.sample(initials, len(initials)))
        emp_code = f"{year_part}{shuffled_initials}{serial_part}"

        existing_emp = db.query(Employee).filter(
            Employee.emp_code == emp_code).first()
        if not existing_emp:
            return emp_code  

        serial_number += 1


def send_email(to_email: str, subject: str, html_content: str):
    try:
        response = resend.Emails.send({
            "from": f"My Org <no-reply@{ORG_DOMAIN}>",
            "to": [to_email],
            "subject": subject,
            "html": html_content
        })
        return response
    except Exception as e:
        print(f"Error sending email: {e}")
        return None
