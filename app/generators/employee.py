from dotenv import load_dotenv
import requests
import random
import time
import os


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


# API Configuration
BASE_URL = os.getenv("BASE_URL")
LOGIN_URL = f"{BASE_URL.replace('/admin', '')}/login/"
NAME_API_URL = "https://random-indian-name-generator.vercel.app/api/random_names"
HEADERS = {"Content-Type": "application/json"}

# Admin Credentials (Replace these with actual credentials)
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


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


# Step 1: Get Auth Token
def get_auth_token():
    try:
        response = requests.post(
            LOGIN_URL, json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            HEADERS["Authorization"] = f"Bearer {access_token}"
            print("✅ Auth token received")
            return access_token
        else:
            print("❌ Login failed:", response.text)
            return None
    except Exception as e:
        print("❌ Error during login:", e)
        return None


# Step 2: Fetch dropdown values for shifts, departments, and designations
def fetch_dropdown_data():
    try:
        shifts = requests.get(f"{BASE_URL}/shifts/", headers=HEADERS).json()
        departments = requests.get(
            f"{BASE_URL}/departments/", headers=HEADERS).json()
        designations = requests.get(
            f"{BASE_URL}/designations/", headers=HEADERS).json()
        print("✅ Dropdown data fetched")
        return shifts, departments, designations
    except Exception as e:
        print("❌ Error fetching dropdown data:", e)
        return [], [], []


# Step 3: Get random Indian names
def get_random_names(count):
    try:
        response = requests.get(f"{NAME_API_URL}/{count}")
        if response.status_code == 200:
            return response.json()
        else:
            print("❌ Error fetching random names")
            return []
    except Exception as e:
        print("❌ Error:", e)
        return []


# Step 4: Get suggested email and employee code
def get_suggested_email_code(name):
    try:
        response = requests.get(
            f"{BASE_URL}/employees/suggest-email-emp-code/{name}", headers=HEADERS)
        data = response.json()
        return data.get("suggested_email"), data.get("suggested_emp_code")
    except Exception as e:
        print(f"❌ Error fetching email/code for {name}:", e)
        return None, None


# Step 5: Create employee
def create_employee(name, shift_id, dept_id, designation_id):
    email, emp_code = get_suggested_email_code(name)
    if not email or not emp_code:
        print(f"⚠️ Skipping {name}, no email/emp_code received.")
        return

    employee_data = {
        "name": name,
        "email": email,
        "emp_code": emp_code,
        "skills" : random.sample(SKILLS, random.randint(2, 15)),
        "experience": random.randint(0, 10),
        "shift_id": shift_id,
        "dept_id": dept_id,
        "designation_id": designation_id
    }

    try:
        response = requests.post(
            f"{BASE_URL}/employees/", json=employee_data, headers=HEADERS)
        if response.status_code in [200, 201]:
            print(f"✅ Successfully added {name} ({email})")
        else:
            print(f"❌ Failed to add {name}: {response.text}")
    except Exception as e:
        print(f"❌ Error adding {name}: {e}")


# Step 6: Generate employees
def generate_employees(count):
    shifts, departments, designations = fetch_dropdown_data()
    if not shifts or not departments or not designations:
        print("❌ Cannot proceed, missing dropdown data.")
        return

    names = get_random_names(count)
    if not names:
        return

    for person in names:
        full_name = f"{person['firstName']} {person['lastName']}"
        shift_id = random.choice(shifts)["id"]
        dept_id = random.choice(departments)["id"]
        designation_id = random.choice(designations)["id"]

        create_employee(full_name, shift_id, dept_id, designation_id)
        time.sleep(1)  # Prevent API rate limits


# Run the script
if __name__ == "__main__":
    auth_token = get_auth_token()
    if auth_token:
        num_employees = int(input("Enter the number of employees to create: "))
        generate_employees(num_employees)
