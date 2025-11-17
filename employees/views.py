from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from calendar import monthrange
import calendar

from .models import User, Employee, Attendance, Salary, Payment, Transaction, Notification
from .forms import UserRegistrationForm, EmployeeForm, AttendanceForm, SalaryForm, PaymentForm


def is_admin(user):
    return user.is_authenticated and user.is_admin_user()


# Public Views
def home(request):
    features = [
        {
            'icon': 'bi-people',
            'title': 'Employee Management',
            'description': 'Maintain detailed employee profiles with salary and banking information.',
        },
        {
            'icon': 'bi-calendar2-check',
            'title': 'Attendance Tracking',
            'description': 'Record attendance, leaves, and half days to drive accurate salary calculations.',
        },
        {
            'icon': 'bi-cash-stack',
            'title': 'Salary Processing',
            'description': 'Calculate, approve, and process monthly salaries with payment history.',
        },
        {
            'icon': 'bi-bar-chart-line',
            'title': 'Insights & Reports',
            'description': 'Track paid vs unpaid salaries and analyse monthly or annual expenditure.',
        },
    ]

    testimonials = [
        {
            'name': 'Finance Teams',
            'quote': '“We are able to close payroll faster and keep every payment transparent.”',
        },
        {
            'name': 'Employees',
            'quote': '“I can check my salary history and status from anywhere, any time.”',
        },
    ]

    return render(request, 'employees/home.html', {
        'features': features,
        'testimonials': testimonials,
    })


# Authentication Views
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'employees/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'employees/login.html')


@login_required
def dashboard(request):
    user = request.user
    context = {}
    
    if user.is_admin_user():
        # Admin Dashboard
        total_employees = Employee.objects.filter(is_active=True).count()
        total_salaries = Salary.objects.filter(is_paid=True).aggregate(
            total=Sum('net_salary')
        )['total'] or 0
        unpaid_salaries = Salary.objects.filter(is_paid=False).aggregate(
            total=Sum('net_salary')
        )['total'] or 0
        
        # Monthly statistics
        current_month = timezone.now().month
        current_year = timezone.now().year
        monthly_paid = Salary.objects.filter(
            is_paid=True, month=current_month, year=current_year
        ).aggregate(total=Sum('net_salary'))['total'] or 0
        
        # Recent payments
        recent_payments = Payment.objects.all()[:10]
        
        # Chart data - Last 6 months
        months_data = []
        salary_data = []
        for i in range(5, -1, -1):
            date = timezone.now() - timedelta(days=30*i)
            month = date.month
            year = date.year
            total = Salary.objects.filter(
                is_paid=True, month=month, year=year
            ).aggregate(total=Sum('net_salary'))['total'] or 0
            months_data.append(calendar.month_abbr[month])
            salary_data.append(float(total))
        
        context = {
            'total_employees': total_employees,
            'total_salaries': total_salaries,
            'unpaid_salaries': unpaid_salaries,
            'monthly_paid': monthly_paid,
            'recent_payments': recent_payments,
            'months_data': months_data,
            'salary_data': salary_data,
        }
    else:
        # Employee Dashboard
        try:
            employee = Employee.objects.get(user=user)
            employee_salaries = Salary.objects.filter(employee=employee).order_by('-year', '-month')[:5]
            unpaid_count = Salary.objects.filter(employee=employee, is_paid=False).count()
            notifications = Notification.objects.filter(employee=employee, is_read=False)[:5]
            
            context = {
                'employee': employee,
                'employee_salaries': employee_salaries,
                'unpaid_count': unpaid_count,
                'notifications': notifications,
            }
        except Employee.DoesNotExist:
            # Employee logged in but no profile linked yet
            # Try to find employee by email or username
            employee = None
            try:
                employee = Employee.objects.filter(email=user.email).first()
                if employee:
                    # Link the employee to the user
                    employee.user = user
                    employee.save()
                    messages.success(request, 'Your employee profile has been linked to your account.')
            except:
                pass
            
            if not employee:
                context = {
                    'no_profile': True,
                    'user': user,
                }
                messages.info(request, 'Your employee profile is not yet linked. Please contact your administrator to link your account.')
            else:
                employee_salaries = Salary.objects.filter(employee=employee).order_by('-year', '-month')[:5]
                unpaid_count = Salary.objects.filter(employee=employee, is_paid=False).count()
                notifications = Notification.objects.filter(employee=employee, is_read=False)[:5]
                
                context = {
                    'employee': employee,
                    'employee_salaries': employee_salaries,
                    'unpaid_count': unpaid_count,
                    'notifications': notifications,
                }
    
    return render(request, 'employees/dashboard.html', context)


# Employee Management Views
@login_required
@user_passes_test(is_admin)
def employee_list(request):
    employees = Employee.objects.all()
    search = request.GET.get('search', '')
    if search:
        employees = employees.filter(
            Q(full_name__icontains=search) |
            Q(employee_id__icontains=search) |
            Q(email__icontains=search)
        )
    return render(request, 'employees/employee_list.html', {'employees': employees, 'search': search})
 

@login_required
@user_passes_test(is_admin)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            # Create user account for employee if needed
            messages.success(request, f'Employee {employee.full_name} created successfully!')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Add Employee'})


@login_required
@user_passes_test(is_admin)
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f'Employee {employee.full_name} updated successfully!')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Edit Employee', 'employee': employee})


@login_required
@user_passes_test(is_admin)
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    salaries = Salary.objects.filter(employee=employee).order_by('-year', '-month')
    return render(request, 'employees/employee_detail.html', {'employee': employee, 'salaries': salaries})


@login_required
@user_passes_test(is_admin)
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.is_active = False
        employee.save()
        messages.success(request, f'Employee {employee.full_name} deactivated successfully!')
        return redirect('employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})


# Attendance Views
@login_required
@user_passes_test(is_admin)
def attendance_list(request):
    attendances = Attendance.objects.all().order_by('-date')
    employee_id = request.GET.get('employee')
    if employee_id:
        attendances = attendances.filter(employee_id=employee_id)
    return render(request, 'employees/attendance_list.html', {'attendances': attendances})


@login_required
@user_passes_test(is_admin)
def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save()
            messages.success(request, 'Attendance recorded successfully!')
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'employees/attendance_form.html', {'form': form, 'title': 'Add Attendance'})


# Salary Views
@login_required
@user_passes_test(is_admin)
def salary_list(request):
    salaries = Salary.objects.all().order_by('-year', '-month')
    employee_id = request.GET.get('employee')
    if employee_id:
        salaries = salaries.filter(employee_id=employee_id)
    return render(request, 'employees/salary_list.html', {'salaries': salaries})


@login_required
@user_passes_test(is_admin)
def salary_create(request):
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            salary = form.save(commit=False)
            # Set base_salary from employee if not provided
            if not salary.base_salary:
                salary.base_salary = salary.employee.base_salary
            salary.calculate_salary()
            salary.save()
            messages.success(request, 'Salary record created successfully!')
            return redirect('salary_list')
    else:
        form = SalaryForm()
    return render(request, 'employees/salary_form.html', {'form': form, 'title': 'Create Salary Record'})


@login_required
@user_passes_test(is_admin)
def salary_calculate(request, pk):
    salary = get_object_or_404(Salary, pk=pk)
    
    try:
        # Calculate based on attendance
        month = salary.month
        year = salary.year
        employee = salary.employee
        
        # Get attendance for the month
        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, monthrange(year, month)[1]).date()
        
        attendances = Attendance.objects.filter(
            employee=employee,
            date__gte=start_date,
            date__lte=end_date
        )
        
        # Calculate days
        total_days = monthrange(year, month)[1]
        days_present = attendances.filter(status='present').count()
        days_absent = attendances.filter(status='absent').count()
        days_on_leave = attendances.filter(status='leave').count()
        half_days = attendances.filter(status='half_day').count()
        
        # Update salary fields
        salary.total_working_days = total_days
        salary.days_present = days_present
        salary.days_absent = days_absent
        salary.days_on_leave = days_on_leave
        salary.half_days = half_days
        salary.base_salary = employee.base_salary
        
        # Calculate salary
        calculated_amount = salary.calculate_salary()
        salary.save()
        
        messages.success(request, f'Salary recalculated successfully! Net Salary: ₹{salary.net_salary:,.2f}')
    except Exception as e:
        messages.error(request, f'Error calculating salary: {str(e)}')
    
    return redirect('salary_detail', pk=pk)


@login_required
def salary_detail(request, pk):
    salary = get_object_or_404(Salary, pk=pk)
    user = request.user
    
    # Check if user has permission
    if not user.is_admin_user() and salary.employee.user != user:
        messages.error(request, 'You do not have permission to view this salary.')
        return redirect('dashboard')
    
    payment = None
    if hasattr(salary, 'payment'):
        payment = salary.payment
    
    return render(request, 'employees/salary_detail.html', {'salary': salary, 'payment': payment})


# Payment Views
@login_required
@user_passes_test(is_admin)
def payment_process(request, salary_id):
    salary = get_object_or_404(Salary, pk=salary_id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.salary = salary
            payment.processed_by = request.user
            payment.save()
            
            # Mark salary as paid
            salary.is_paid = True
            salary.save()
            
            # Create transaction
            Transaction.objects.create(
                employee=salary.employee,
                payment=payment,
                amount=salary.net_salary,
                transaction_date=payment.payment_date,
                description=f"Salary payment for {salary.get_month_display()} {salary.year}"
            )
            
            # Create notification
            Notification.objects.create(
                employee=salary.employee,
                notification_type='salary_paid',
                title='Salary Paid',
                message=f'Your salary for {salary.get_month_display()} {salary.year} has been processed. Amount: ₹{salary.net_salary}'
            )
            
            messages.success(request, 'Payment processed successfully!')
            return redirect('salary_detail', pk=salary_id)
    else:
        form = PaymentForm(initial={'payment_date': timezone.now().date()})
    
    return render(request, 'employees/payment_form.html', {'form': form, 'salary': salary})


@login_required
@user_passes_test(is_admin)
def payment_mark_unpaid(request, salary_id):
    salary = get_object_or_404(Salary, pk=salary_id)
    if request.method == 'POST':
        salary.is_paid = False
        if hasattr(salary, 'payment'):
            salary.payment.delete()
        salary.save()
        messages.success(request, 'Salary marked as unpaid.')
    return redirect('salary_detail', pk=salary_id)


# Transaction History
@login_required
def transaction_history(request, employee_id=None):
    user = request.user
    
    if user.is_admin_user():
        if employee_id:
            employee = get_object_or_404(Employee, pk=employee_id)
            transactions = Transaction.objects.filter(employee=employee).order_by('-transaction_date')
        else:
            transactions = Transaction.objects.all().order_by('-transaction_date')
    else:
        employee = get_object_or_404(Employee, user=user)
        transactions = Transaction.objects.filter(employee=employee).order_by('-transaction_date')
    
    return render(request, 'employees/transaction_history.html', {
        'transactions': transactions,
        'employee': employee if employee_id or not user.is_admin_user() else None
    })


# Reports
@login_required
@user_passes_test(is_admin)
def reports(request):
    context = {}
    
    # Monthly Report
    if request.GET.get('type') == 'monthly':
        month = int(request.GET.get('month', timezone.now().month))
        year = int(request.GET.get('year', timezone.now().year))
        
        salaries = Salary.objects.filter(month=month, year=year)
        total_expenditure = salaries.filter(is_paid=True).aggregate(
            total=Sum('net_salary')
        )['total'] or 0
        
        context.update({
            'report_type': 'monthly',
            'month': month,
            'year': year,
            'salaries': salaries,
            'total_expenditure': total_expenditure,
        })
    
    # Annual Report
    elif request.GET.get('type') == 'annual':
        year = int(request.GET.get('year', timezone.now().year))
        
        salaries = Salary.objects.filter(year=year, is_paid=True)
        total_expenditure = salaries.aggregate(total=Sum('net_salary'))['total'] or 0
        
        # Monthly breakdown
        monthly_data = []
        for month in range(1, 13):
            month_total = salaries.filter(month=month).aggregate(
                total=Sum('net_salary')
            )['total'] or 0
            monthly_data.append({
                'month': calendar.month_name[month],
                'total': month_total
            })
        
        context.update({
            'report_type': 'annual',
            'year': year,
            'salaries': salaries,
            'total_expenditure': total_expenditure,
            'monthly_data': monthly_data,
        })
    
    return render(request, 'employees/reports.html', context)


# Notifications
@login_required
def notifications(request):
    user = request.user
    
    if user.is_admin_user():
        notifications_list = Notification.objects.all().order_by('-created_at')
    else:
        employee = get_object_or_404(Employee, user=user)
        notifications_list = Notification.objects.filter(employee=employee).order_by('-created_at')
    
    return render(request, 'employees/notifications.html', {'notifications': notifications_list})


@login_required
def notification_mark_read(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id)
    user = request.user
    
    # Check permission
    if not user.is_admin_user() and notification.employee.user != user:
        messages.error(request, 'You do not have permission.')
        return redirect('dashboard')
    
    notification.is_read = True
    notification.save()
    return redirect('notifications')
