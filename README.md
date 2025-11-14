# PayEase - Employee Payment Platform

A comprehensive Django-based Employee Payment Platform with features for managing employees, salaries, payments, attendance, and generating reports.

## Features

- **User Authentication**: Login/Registration with Admin and Employee roles
- **Employee Management**: Add, edit, and view employee details (name, ID, salary, bank info)
- **Salary Calculation**: Calculate pay based on working days, leaves, or attendance
- **Payment Processing**: Mark salary as paid/unpaid and record payment date/method
- **Dashboard**: Show total employees, paid/unpaid salaries, and summary charts
- **Transaction History**: View previous payments for each employee
- **Reports**: Monthly/annual salary expenditure reports
- **Notifications**: Notify employees when salary is processed

## Installation

1. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

3. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

4. **Access the application**:
   - Open your browser and go to: `http://127.0.0.1:8000/`
   - Register a new user or login with your superuser credentials

## Usage

### Admin Features

1. **Employee Management**:
   - Navigate to "Employees" to add, edit, or view employees
   - Each employee requires: ID, name, email, phone, bank details, and base salary

2. **Attendance Management**:
   - Record daily attendance for employees
   - Track present, absent, leave, and half-day status

3. **Salary Management**:
   - Create salary records for each month
   - Calculate salary based on attendance
   - View detailed salary breakdowns

4. **Payment Processing**:
   - Process payments for calculated salaries
   - Record payment method, date, and transaction ID
   - Mark salaries as paid/unpaid

5. **Reports**:
   - Generate monthly salary expenditure reports
   - Generate annual salary expenditure reports with monthly breakdown

### Employee Features

1. **Dashboard**:
   - View personal information and salary history
   - Check payment status
   - View recent notifications

2. **Notifications**:
   - Receive notifications when salary is processed
   - Mark notifications as read

## Models

- **User**: Custom user model with Admin/Employee roles
- **Employee**: Employee profile with personal and bank information
- **Attendance**: Daily attendance records
- **Salary**: Monthly salary calculations
- **Payment**: Payment processing records
- **Transaction**: Transaction history
- **Notification**: System notifications for employees

## Technology Stack

- **Backend**: Django 5.2.8
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)
- **PDF Generation**: ReportLab
- **Frontend**: Bootstrap 5, Chart.js
- **Icons**: Bootstrap Icons

## Project Structure (PayEase)

```
django_project3/
├── employees/              # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Form definitions
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin configuration
│   └── templates/         # HTML templates
├── payment_management/     # Project settings
│   ├── settings.py        # Django settings
│   └── urls.py            # Main URL configuration
└── manage.py              # Django management script
```

## Default Credentials

After creating a superuser, you can:
- Login as admin to access all features
- Register new users (both admin and employee roles available)
- Create employee profiles linked to user accounts

## Notes

- The system uses SQLite by default for development
- For production, consider switching to PostgreSQL or MySQL
- All sensitive data should be properly secured in production
- Make sure to set `DEBUG = False` and configure `ALLOWED_HOSTS` for production

## License

PayEase is open source and available for educational purposes.


