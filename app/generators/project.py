import os
import random
from datetime import datetime, timedelta
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from app.models.project import ProjectStatus, ProjectPriority


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")
engine = create_engine(DATABASE_URL)

# Sample Data
PROJECT_NAMES = [
    "AI-based Attendance Tracker", "Cloud Migration System", "Employee Wellness Dashboard",
    "Predictive Analytics Tool", "HR Chatbot", "IoT-based Office Monitoring",
    "Workflow Automation", "Task Management System", "Skill Matching Platform",
    "Smart Resume Parser", "AI-Powered Recruitment System", "Employee Sentiment Analyzer",
    "Time Tracking and Productivity Tool", "Cybersecurity Risk Assessment",
    "Automated Payroll System", "Hybrid Work Management Platform",
    "Real-Time Collaboration Suite", "Automated Code Review System",
    "Virtual Reality (VR) Training Simulator", "AI-Powered Document Summarization",
    "Blockchain-Based Employee Credentials Verification", "E-learning Content Recommendation Engine",
    "Automated IT Asset Management", "Voice-Controlled Virtual Assistant",
    "Smart Meeting Scheduling System", "AI-Powered Contract Analyzer",
    "Remote Work Monitoring & Reporting", "Automated Leave Management System",
    "Employee Energy Consumption Tracker", "Intelligent Chatbot for Workplace Queries"
]

DESCRIPTIONS = [
    "A system that tracks attendance using facial recognition.",
    "Migration of company services to a secure cloud environment.",
    "Dashboard for tracking employee wellness and work-life balance.",
    "Predictive analytics for employee performance and absenteeism.",
    "AI chatbot for HR queries and employee support.",
    "IoT sensors monitoring office conditions and power usage.",
    "Automation of repetitive workflows to improve efficiency.",
    "A task management system to assign and track employee work.",
    "A platform that matches employees to projects based on skills.",
    "A resume parser using NLP to extract key details from resumes.",
    "AI-powered recruitment tool that shortlists candidates based on skills and experience.",
    "Sentiment analysis engine to gauge employee satisfaction from feedback data.",
    "A system for tracking work hours and productivity across teams.",
    "Cybersecurity system to assess and mitigate organizational risks.",
    "Payroll automation platform integrating with attendance and HR records.",
    "A hybrid work scheduling platform for remote and in-office employees.",
    "A real-time collaboration suite with task tracking and document sharing.",
    "Automated tool for reviewing and suggesting improvements in code.",
    "VR-based training simulator for onboarding and upskilling employees.",
    "AI-powered tool for summarizing lengthy documents into key points.",
    "Blockchain-based verification system for employee credentials and certifications.",
    "E-learning recommendation engine suggesting courses based on job roles.",
    "Automated system to track and manage IT assets within an organization.",
    "Voice-controlled virtual assistant to handle workplace queries.",
    "An intelligent meeting scheduler that suggests optimal meeting times.",
    "AI-powered contract analyzer to detect risks and inconsistencies in agreements.",
    "A remote work monitoring system that ensures productivity and compliance.",
    "A leave management system automating approval workflows and tracking absences.",
    "An employee energy consumption tracking tool promoting sustainable practices.",
    "An NLP-based chatbot for workplace FAQs, HR support, and IT helpdesk."
]

STATUSES = list(ProjectStatus)  # ✅ Use Enum directly
PRIORITIES = list(ProjectPriority)  # ✅ Use Enum directly
SKILLS = [
    "Python", "React", "SQL", "FastAPI", "Machine Learning", "Django", "Flutter", "Cloud Computing",
    "NLP", "Blockchain", "Cybersecurity", "TensorFlow", "PyTorch", "AWS", "Azure", "Google Cloud",
    "JavaScript", "TypeScript", "Node.js", "GraphQL", "Docker", "Kubernetes", "Jenkins", "CI/CD",
    "Rust", "Go", "Java", "Spring Boot", "C++", "C#", "Swift", "Kotlin", "MongoDB", "PostgreSQL",
    "MySQL", "Redis", "Elasticsearch", "Kafka", "RabbitMQ", "Big Data", "Hadoop", "Spark",
    "TensorFlow.js", "OpenCV", "Pandas", "Scikit-learn", "Keras", "LangChain", "LlamaIndex",
    "Power BI", "Tableau", "Excel Automation", "Graph Analytics", "Web Scraping", "REST API Design",
    "OAuth2", "Zero Trust Security", "Penetration Testing", "Digital Forensics", "RPA (UiPath, Blue Prism)",
    "Unity 3D", "Unreal Engine", "Metaverse Development", "Voice Recognition", "Chatbot Development",
    "Remote Sensing", "IoT Security", "Edge Computing", "5G Networks", "Quantum Computing Basics"
]
TEAM_SIZE_RANGE = (2, 10)
EXPERIENCE_RANGE = (0, 5)

# Function to generate a random date within a range


def random_date(start_date, end_date):
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

# Generate and insert projects


def generate_projects(num_projects=10):
    with engine.connect() as conn:
            for _ in range(num_projects):
                try:
                    trans = conn.begin()
                    project_code = f"PRJ-{random.randint(1000, 9999)}"
                    name = random.choice(PROJECT_NAMES)
                    description = random.choice(DESCRIPTIONS)

                    # ✅ Convert Enum to string
                    status = random.choice(STATUSES).value
                    # ✅ Convert Enum to string
                    priority = random.choice(PRIORITIES).value

                    max_team_size = random.randint(*TEAM_SIZE_RANGE)
                    required_skills = random.sample(SKILLS, random.randint(2, 4))
                    min_experience = random.randint(*EXPERIENCE_RANGE)

                    # Define start and end dates
                    start_date = random_date(
                        datetime(2024, 1, 1), datetime(2025, 1, 1))
                    end_date = start_date + timedelta(days=random.randint(30, 180))

                    # Insert into DB
                    conn.execute(text("""
                    INSERT INTO projects (id, code, name, description, start_date, end_date, status, priority, max_team_size, required_skills, min_experience)
                    VALUES (gen_random_uuid(), :code, :name, :description, :start_date, :end_date, :status, :priority, :max_team_size, :required_skills, :min_experience)
                """), {
                        "code": project_code,
                        "name": name,
                        "description": description,
                        "start_date": start_date.date(),
                        "end_date": end_date.date(),
                        "status": status.upper(),  
                        "priority": priority.upper(),
                        "max_team_size": max_team_size,
                        "required_skills": required_skills,
                        "min_experience": min_experience
                    })
                    time.sleep(0.2)
                    trans.commit()
                except Exception as e:
                    trans.rollback()
                    print(f"❌ Error inserting projects: {e}")
                
            print(f"✅ Successfully inserted {num_projects} dummy projects.")



# Run script
if __name__ == "__main__":
    num_projects = int(
        input("Enter the number of dummy projects to generate: "))
    generate_projects(num_projects)
