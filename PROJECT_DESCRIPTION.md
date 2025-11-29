# PayEase - Employee Payment Management System

## Project Description

**PayEase** is a comprehensive Django-based web application designed for managing employee payroll, attendance tracking, and payment processing. It provides a complete solution for organizations to handle employee management, calculate salaries based on attendance, process payments, and generate detailed reports. The system supports role-based access control with separate interfaces for administrators and employees.

---

## Core Functionalities

### 1. **User Authentication & Authorization**
- User registration with role selection (Admin/Employee)
- Secure login/logout functionality
- Role-based access control ensuring employees can only access their own data
- Custom user model extending Django's AbstractUser

### 2. **Employee Management**
- Create, view, edit, and deactivate employee profiles
- Store comprehensive employee information including:
  - Personal details (name, email, phone, address)
  - Employment details (ID, designation, department, date of joining)
  - Banking information (bank name, account number, IFSC code)
  - Base salary configuration
- Link employee profiles to user accounts
- Search and filter employees

### 3. **Attendance Tracking**
- Record daily attendance for employees
- Track multiple attendance statuses:
  - Present
  - Absent
  - Leave
  - Half Day
- Record check-in and check-out times
- Add notes for attendance records
- Prevent duplicate attendance entries for the same employee and date

### 4. **Salary Calculation & Management**
- Create monthly salary records for employees
- Automatic salary calculation based on:
  - Total working days in the month
  - Days present
  - Days absent
  - Days on leave
  - Half days (counted as 0.5 days)
- Formula: `(Present Days + Half Days × 0.5) × (Base Salary / Total Working Days)`
- Support for allowances and deductions
- Calculate net salary: `Calculated Amount + Allowances - Deductions`
- Recalculate salaries based on updated attendance data

### 5. **Payment Processing**
- Process payments for calculated salaries
- Record payment details:
  - Payment date
  - Payment method (Bank Transfer, Cash, Cheque, UPI, Other)
  - Transaction ID
  - Notes
- Mark salaries as paid/unpaid
- Track who processed each payment
- Automatic transaction history creation

### 6. **Transaction History**
- View complete payment history for employees
- Filter transactions by employee (for admins)
- Display transaction details including amount, date, and description
- Maintain audit trail of all financial transactions

### 7. **Dashboard & Analytics**
- **Admin Dashboard:**
  - Total active employees count
  - Total paid salaries summary
  - Unpaid salaries summary
  - Current month's paid salaries
  - Recent payments list
  - Visual charts showing salary trends over last 6 months (using Chart.js)
  
- **Employee Dashboard:**
  - Personal employee information
  - Recent salary history (last 5 records)
  - Unpaid salary count
  - Recent notifications

### 8. **Reports Generation**
- **Monthly Reports:**
  - View all salaries for a specific month
  - Calculate total monthly expenditure
  - Filter by paid/unpaid status
  
- **Annual Reports:**
  - View all salaries for a specific year
  - Calculate total annual expenditure
  - Monthly breakdown showing expenditure per month

### 9. **Notification System**
- Automatic notifications when salary is processed
- Notification types:
  - Salary Paid
  - Salary Pending
  - Payment Processed
- Mark notifications as read/unread
- Separate notification views for admins and employees

---

## Key Features

### Security Features
- Password validation and secure authentication
- CSRF protection
- Role-based permission system
- User-specific data access restrictions

### User Experience Features
- Responsive Bootstrap 5 UI design
- Intuitive navigation with role-based menus
- Search and filter capabilities
- Visual data representation with charts
- Success/error message notifications
- Clean, modern interface with Bootstrap Icons

### Data Management Features
- Comprehensive data models with relationships
- Automatic timestamp tracking (created_at, updated_at)
- Soft delete functionality (employee deactivation)
- Unique constraints to prevent data duplication
- Efficient database queries with proper indexing

### Administrative Features
- Django admin interface integration
- Custom admin configurations for all models
- Advanced filtering and search in admin panel
- Date hierarchy navigation in admin

---

## Technology Stack

- **Backend Framework:** Django 5.2.5
- **Database:** SQLite (default, configurable for PostgreSQL/MySQL)
- **Frontend:**
  - Bootstrap 5 (UI framework)
  - Chart.js (data visualization)
  - Bootstrap Icons
- **PDF Generation:** ReportLab (for future report exports)
- **Static Files:** WhiteNoise (for production static file serving)
- **Additional Libraries:**
  - Various data processing libraries (pandas, numpy)
  - NLP libraries (spacy, nltk) - likely for resume parsing features
  - Streamlit - for potential analytics dashboards

---

## File Structure

```
django_project3/
│
├── PayEase/                          # Main project directory
│   │
│   ├── manage.py                     # Django management script
│   ├── db.sqlite3                    # SQLite database file
│   ├── README.md                     # Project documentation
│   ├── requirements.txt              # Python dependencies
│   │
│   ├── employees/                    # Main application module
│   │   ├── __init__.py
│   │   ├── admin.py                  # Django admin configurations
│   │   ├── apps.py                   # App configuration
│   │   ├── forms.py                  # Form definitions for all models
│   │   ├── models.py                 # Database models (User, Employee, Attendance, Salary, Payment, Transaction, Notification)
│   │   ├── views.py                  # View functions (all business logic)
│   │   ├── urls.py                   # URL routing for employees app
│   │   ├── tests.py                  # Unit tests
│   │   │
│   │   └── templates/                # HTML templates
│   │       └── employees/
│   │           ├── base.html         # Base template with navigation
│   │           ├── home.html         # Landing page
│   │           ├── login.html        # Login page
│   │           ├── register.html     # Registration page
│   │           ├── dashboard.html    # Main dashboard (role-based)
│   │           ├── employee_list.html
│   │           ├── employee_form.html
│   │           ├── employee_detail.html
│   │           ├── employee_confirm_delete.html
│   │           ├── attendance_list.html
│   │           ├── attendance_form.html
│   │           ├── salary_list.html
│   │           ├── salary_form.html
│   │           ├── salary_detail.html
│   │           ├── payment_form.html
│   │           ├── transaction_history.html
│   │           ├── reports.html
│   │           └── notifications.html
│   │
│   ├── payment_management/           # Django project settings
│   │   ├── __init__.py
│   │   ├── settings.py               # Django settings (database, apps, middleware, etc.)
│   │   ├── urls.py                   # Main URL configuration
│   │   ├── wsgi.py                   # WSGI configuration for deployment
│   │   └── asgi.py                   # ASGI configuration for async support
│   │
│   └── venv/                         # Python virtual environment
│       └── [virtual environment files]
│
└── PROJECT_DESCRIPTION.md            # This file
```

---

## Database Models

### 1. **User** (Custom User Model)
- Extends Django's AbstractUser
- Fields: username, email, role (admin/employee), phone, created_at
- Methods: `is_admin_user()`

### 2. **Employee**
- One-to-one relationship with User (optional)
- Fields: employee_id, full_name, email, phone, address, date_of_joining, designation, department, bank_name, account_number, ifsc_code, base_salary, is_active, timestamps

### 3. **Attendance**
- Foreign key to Employee
- Fields: date, status, check_in, check_out, notes
- Unique constraint: (employee, date)

### 4. **Salary**
- Foreign key to Employee
- Fields: month, year, base_salary, attendance details (total_working_days, days_present, days_absent, days_on_leave, half_days), calculated_amount, allowances, deductions, net_salary, is_paid
- Unique constraint: (employee, month, year)
- Methods: `calculate_salary()`, `get_month_display()`

### 5. **Payment**
- One-to-one relationship with Salary
- Fields: payment_date, payment_method, transaction_id, notes, processed_by (User)
- Links salary payment to transaction records

### 6. **Transaction**
- Foreign keys to Employee and Payment
- Fields: amount, transaction_date, description
- Maintains complete payment history

### 7. **Notification**
- Foreign key to Employee
- Fields: notification_type, title, message, is_read, created_at
- Used for system notifications to employees

---

## URL Routes

### Public Routes
- `/` - Home page
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout

### Dashboard
- `/dashboard/` - Main dashboard (role-based view)

### Employee Management (Admin Only)
- `/employees/` - List all employees
- `/employees/create/` - Create new employee
- `/employees/<id>/` - Employee details
- `/employees/<id>/edit/` - Edit employee
- `/employees/<id>/delete/` - Deactivate employee

### Attendance (Admin Only)
- `/attendance/` - List all attendance records
- `/attendance/create/` - Record attendance

### Salary Management
- `/salaries/` - List all salaries (Admin) / Own salaries (Employee)
- `/salaries/create/` - Create salary record (Admin only)
- `/salaries/<id>/` - Salary details
- `/salaries/<id>/calculate/` - Recalculate salary (Admin only)

### Payment Processing (Admin Only)
- `/salaries/<id>/payment/` - Process payment
- `/salaries/<id>/mark-unpaid/` - Mark salary as unpaid

### Transactions
- `/transactions/` - All transactions (Admin) / Own transactions (Employee)
- `/transactions/<employee_id>/` - Employee-specific transactions

### Reports (Admin Only)
- `/reports/?type=monthly&month=X&year=Y` - Monthly report
- `/reports/?type=annual&year=Y` - Annual report

### Notifications
- `/notifications/` - View notifications
- `/notifications/<id>/read/` - Mark notification as read

---

## Key Business Logic

### Salary Calculation Algorithm
1. Calculate salary per day: `Base Salary / Total Working Days`
2. Calculate present days value: `Days Present × Salary Per Day`
3. Calculate half days value: `Half Days × 0.5 × Salary Per Day`
4. Calculate base amount: `Present Days Value + Half Days Value`
5. Apply allowances and deductions
6. Final net salary: `Base Amount + Allowances - Deductions`

### Payment Processing Flow
1. Admin creates salary record for employee and month
2. System calculates salary based on attendance (or manual entry)
3. Admin processes payment with payment details
4. System marks salary as paid
5. System creates transaction record
6. System sends notification to employee
7. Employee can view payment status and details

---

## Installation & Setup

1. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access application:**
   - Open browser: `http://127.0.0.1:8000/`
   - Login with superuser or register new account

---

## Future Enhancements (Potential)

Based on the dependencies in requirements.txt, potential future features might include:
- Resume/CV parsing using pyresparser
- Advanced analytics with Streamlit dashboards
- PDF report generation with ReportLab
- Data visualization with Plotly
- Natural language processing features

---

## Security Considerations

- Change `SECRET_KEY` in production
- Set `DEBUG = False` for production
- Configure `ALLOWED_HOSTS` properly
- Use PostgreSQL or MySQL for production database
- Implement proper backup strategies
- Add rate limiting for authentication
- Use HTTPS in production
- Regular security updates for dependencies

---

## License

PayEase is open source and available for educational purposes.

