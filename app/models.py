from app import db
from datetime import datetime
import uuid

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employees = db.relationship('Employee', backref='department', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hire_date = db.Column(db.DateTime, default=datetime.utcnow)
    job_title = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    performance_rating = db.Column(db.Float, nullable=True)
    active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'hire_date': self.hire_date.strftime('%Y-%m-%d'),
            'job_title': self.job_title,
            'department_id': self.department_id,
            'department_name': self.department.name,
            'salary': self.salary,
            'performance_rating': self.performance_rating,
            'active': self.active
        }
