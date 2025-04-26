from flask import Blueprint, jsonify, request, render_template
from app.models import Department, Employee
from app import db
from app.data_generator import generate_employees, generate_departments
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def index():
    return render_template('index.html')

@api_bp.route('/api')
def api_info():
    return jsonify({
        'name': 'Employee Data API',
        'version': '1.0',
        'documentation': '/swagger',
        'endpoints': {
            'generate_data': '/api/generate-data',
            'employees': '/api/employees',
            'departments': '/api/departments',
            'analytics': {
                'employees_by_department': '/api/analytics/employees-by-department',
                'salary_distribution': '/api/analytics/salary-distribution',
                'tenure_distribution': '/api/analytics/tenure-distribution',
                'performance_by_department': '/api/analytics/performance-by-department'
            },
            'visualizations': {
                'employees_by_department': '/api/visualizations/employees-by-department',
                'salary_distribution': '/api/visualizations/salary-distribution'
            }
        }
    })

@api_bp.route('/api/generate-data', methods=['POST'])
def generate_data():
    data = request.get_json() or {}
    num_employees = data.get('num_employees', 100)
    
    departments = Department.query.all()
    if not departments:
        departments = generate_departments()
    
    employees = generate_employees(num_employees)
    
    return jsonify({
        'message': f'Successfully generated {num_employees} employee records',
        'department_count': len(departments),
        'employee_count': len(employees)
    }), 201

@api_bp.route('/api/employees', methods=['GET'])
def get_employees():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    employees = Employee.query.paginate(page=page, per_page=per_page)
    
    data = {
        'items': [item.to_dict() for item in employees.items],
        'meta': {
            'page': employees.page,
            'per_page': employees.per_page,
            'total_pages': employees.pages,
            'total_items': employees.total
        }
    }
    
    return jsonify(data)

@api_bp.route('/api/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get_or_404(id)
    return jsonify(employee.to_dict())

@api_bp.route('/api/departments', methods=['GET'])
def get_departments():
    departments = Department.query.all()
    return jsonify([dept.to_dict() for dept in departments])

@api_bp.route('/api/departments/<int:id>/employees', methods=['GET'])
def get_department_employees(id):
    department = Department.query.get_or_404(id)
    employees = Employee.query.filter_by(department_id=id).all()
    
    return jsonify({
        'department': department.to_dict(),
        'employees': [emp.to_dict() for emp in employees]
    })

@api_bp.route('/api/analytics/employees-by-department', methods=['GET'])
def get_employees_by_department():
    departments = Department.query.all()
    data = []
    
    for dept in departments:
        count = Employee.query.filter_by(department_id=dept.id).count()
        data.append({
            'department': dept.name,
            'employee_count': count
        })
    
    return jsonify(data)

@api_bp.route('/api/analytics/salary-distribution', methods=['GET'])
def get_salary_distribution():
    employees = Employee.query.all()
    salary_data = [emp.salary for emp in employees]
    
    avg_salary = sum(salary_data) / len(salary_data) if salary_data else 0
    min_salary = min(salary_data) if salary_data else 0
    max_salary = max(salary_data) if salary_data else 0
    
    ranges = [
        {'range': '0-50k', 'min': 0, 'max': 50000, 'count': 0},
        {'range': '50k-75k', 'min': 50000, 'max': 75000, 'count': 0},
        {'range': '75k-100k', 'min': 75000, 'max': 100000, 'count': 0},
        {'range': '100k-125k', 'min': 100000, 'max': 125000, 'count': 0},
        {'range': '125k-150k', 'min': 125000, 'max': 150000, 'count': 0},
        {'range': '150k+', 'min': 150000, 'max': 99999999, 'count': 0}
    ]
    
    for salary in salary_data:
        for r in ranges:
            if r['min'] <= salary < r['max']:
                r['count'] += 1
                break
    
    return jsonify({
        'statistics': {
            'average_salary': avg_salary,
            'min_salary': min_salary,
            'max_salary': max_salary,
            'total_employees': len(salary_data)
        },
        'distribution': ranges
    })

@api_bp.route('/api/analytics/tenure-distribution', methods=['GET'])
def get_tenure_distribution():
    employees = Employee.query.all()
    now = pd.Timestamp.now()
    
    tenure_data = []
    for emp in employees:
        hire_date = pd.Timestamp(emp.hire_date)
        tenure_years = (now - hire_date).days / 365.25
        tenure_data.append({
            'employee_id': emp.employee_id,
            'name': f"{emp.first_name} {emp.last_name}",
            'hire_date': emp.hire_date.strftime('%Y-%m-%d'),
            'tenure_years': round(tenure_years, 2)
        })
    
    tenure_buckets = [
        {'range': '<1 year', 'min': 0, 'max': 1, 'count': 0},
        {'range': '1-2 years', 'min': 1, 'max': 2, 'count': 0},
        {'range': '2-3 years', 'min': 2, 'max': 3, 'count': 0},
        {'range': '3-4 years', 'min': 3, 'max': 4, 'count': 0},
        {'range': '4-5 years', 'min': 4, 'max': 5, 'count': 0},
        {'range': '5+ years', 'min': 5, 'max': 9999999999999, 'count': 0}
    ]
    
    for emp in tenure_data:
        for bucket in tenure_buckets:
            if bucket['min'] <= emp['tenure_years'] < bucket['max']:
                bucket['count'] += 1
                break
    
    return jsonify({
        'employees': tenure_data,
        'distribution': tenure_buckets
    })

@api_bp.route('/api/analytics/performance-by-department', methods=['GET'])
def get_performance_by_department():
    departments = Department.query.all()
    data = []
    
    for dept in departments:
        employees = Employee.query.filter_by(department_id=dept.id).all()
        if employees:
            avg_performance = sum(emp.performance_rating or 0 for emp in employees) / len(employees)
        else:
            avg_performance = 0
            
        data.append({
            'department': dept.name,
            'employee_count': len(employees),
            'average_performance': round(avg_performance, 2)
        })
    
    return jsonify(data)

@api_bp.route('/api/visualizations/employees-by-department', methods=['GET'])
def viz_employees_by_dept():
    departments = Department.query.all()
    dept_names = []
    emp_counts = []
    
    for dept in departments:
        count = Employee.query.filter_by(department_id=dept.id).count()
        dept_names.append(dept.name)
        emp_counts.append(count)
    
    df = pd.DataFrame({
        'Department': dept_names,
        'Employee Count': emp_counts
    })
    
    plt.figure(figsize=(10, 6))
    plt.bar(df['Department'], df['Employee Count'], color='skyblue')
    plt.title('Employees by Department')
    plt.xlabel('Department')
    plt.ylabel('Number of Employees')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graphic = base64.b64encode(image_png).decode('utf-8')
    
    return jsonify({
        'chart_data': {
            'departments': dept_names,
            'counts': emp_counts
        },
        'image': graphic
    })

@api_bp.route('/api/visualizations/salary-distribution', methods=['GET'])
def viz_salary_distribution():
    employees = Employee.query.all()
    salaries = [emp.salary for emp in employees]
    
    plt.figure(figsize=(10, 6))
    plt.hist(salaries, bins=20, color='lightgreen', edgecolor='black')
    plt.title('Salary Distribution')
    plt.xlabel('Salary ($)')
    plt.ylabel('Number of Employees')
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graphic = base64.b64encode(image_png).decode('utf-8')
    
    return jsonify({
        'chart_data': {
            'min_salary': min(salaries) if salaries else 0,
            'max_salary': max(salaries) if salaries else 0,
            'avg_salary': sum(salaries) / len(salaries) if salaries else 0,
        },
        'image': graphic
    })
