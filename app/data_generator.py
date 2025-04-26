from faker import Faker
from app.models import Department, Employee
from app import db
import random
from datetime import datetime, timedelta

fake = Faker()

DEPARTMENTS = [
    "Engineering",
    "Human Resources",
    "Sales",
    "Marketing",
    "Finance",
    "Operations",
    "Customer Support",
    "Research & Development",
    "Legal",
    "Executive"
]

JOB_TITLES = {
    "Engineering": ["Software Engineer", "DevOps Engineer", "Quality Assurance Engineer", "Data Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer", "Engineering Manager"],
    "Human Resources": ["HR Specialist", "Recruiter", "HR Manager", "Benefits Coordinator", "Talent Acquisition Specialist"],
    "Sales": ["Sales Representative", "Account Executive", "Sales Manager", "Business Development Representative", "Sales Director"],
    "Marketing": ["Marketing Specialist", "Content Writer", "Social Media Manager", "Marketing Analyst", "Brand Manager"],
    "Finance": ["Financial Analyst", "Accountant", "Controller", "Finance Manager", "Treasury Analyst"],
    "Operations": ["Operations Manager", "Business Analyst", "Project Manager", "Operations Analyst", "Process Improvement Specialist"],
    "Customer Support": ["Customer Support Representative", "Customer Success Manager", "Technical Support Specialist", "Support Team Lead"],
    "Research & Development": ["Research Scientist", "Product Developer", "Innovation Manager", "R&D Specialist"],
    "Legal": ["Legal Counsel", "Compliance Officer", "Legal Assistant", "Contract Specialist"],
    "Executive": ["CEO", "CTO", "CFO", "COO", "CIO", "CMO", "CHRO"]
}

SALARY_RANGES = {
    "Engineering": {"min": 70000, "max": 150000},
    "Human Resources": {"min": 50000, "max": 120000},
    "Sales": {"min": 60000, "max": 140000},
    "Marketing": {"min": 55000, "max": 130000},
    "Finance": {"min": 65000, "max": 140000},
    "Operations": {"min": 55000, "max": 120000},
    "Customer Support": {"min": 45000, "max": 90000},
    "Research & Development": {"min": 70000, "max": 160000},
    "Legal": {"min": 75000, "max": 180000},
    "Executive": {"min": 120000, "max": 300000}
}

def generate_departments():
    """Generate department data"""
    departments = []
    for dept_name in DEPARTMENTS:
        department = Department(name=dept_name)
        departments.append(department)
    
    db.session.add_all(departments)
    db.session.commit()
    return departments

def generate_employees(num_employees=100):
    """Generate employee data"""
    departments = Department.query.all()
    if not departments:
        departments = generate_departments()
    
    employees = []
    for _ in range(num_employees):
        department = random.choice(departments)
        job_title = random.choice(JOB_TITLES[department.name])
        
        hire_date = datetime.utcnow() - timedelta(days=random.randint(0, 5*365))
        
        salary_range = SALARY_RANGES[department.name]
        salary = round(random.uniform(salary_range["min"], salary_range["max"]), 2)
        
        performance_rating = round(random.uniform(1.0, 5.0), 1)
        
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        random_suffix = ''.join(random.choices('0123456789', k=5))
        email = f"{first_name.lower()}.{last_name.lower()}.{random_suffix}@company.com"
        
        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            hire_date=hire_date,
            job_title=job_title,
            department_id=department.id,
            salary=salary,
            performance_rating=performance_rating,
            active=random.random() > 0.1  
        )
        employees.append(employee)
    
    db.session.add_all(employees)
    db.session.commit()
    return employees
