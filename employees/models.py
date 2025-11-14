from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from decimal import Decimal


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    def is_admin_user(self):
        return self.role == 'admin'


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile', null=True, blank=True)
    employee_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    date_of_joining = models.DateField()
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    
    # Bank Information
    bank_name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=20)
    
    # Salary Information
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} ({self.employee_id})"


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'Leave'),
        ('half_day', 'Half Day'),
    ], default='present')
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['employee', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.employee.full_name} - {self.date} - {self.status}"


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salaries')
    month = models.IntegerField()  # 1-12
    year = models.IntegerField()
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Attendance details
    total_working_days = models.IntegerField(default=0)
    days_present = models.IntegerField(default=0)
    days_absent = models.IntegerField(default=0)
    days_on_leave = models.IntegerField(default=0)
    half_days = models.IntegerField(default=0)
    
    # Calculations
    salary_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    calculated_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Deductions and Allowances
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Final amount
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['employee', 'month', 'year']
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.employee.full_name} - {self.get_month_display()} {self.year}"

    def get_month_display(self):
        months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        return months[self.month] if 1 <= self.month <= 12 else str(self.month)

    def calculate_salary(self):
        """Calculate salary based on attendance"""
        if self.total_working_days == 0:
            return Decimal('0.00')
        
        self.salary_per_day = self.base_salary / Decimal(self.total_working_days)
        
        # Calculate based on present days
        present_days = Decimal(self.days_present)
        half_day_value = Decimal(self.half_days) * Decimal('0.5')
        
        self.calculated_amount = (present_days + half_day_value) * self.salary_per_day
        self.net_salary = self.calculated_amount + self.allowances - self.deductions
        
        return self.net_salary


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('upi', 'UPI'),
        ('other', 'Other'),
    ]
    
    salary = models.OneToOneField(Salary, on_delete=models.CASCADE, related_name='payment')
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='processed_payments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f"Payment for {self.salary.employee.full_name} - {self.payment_date}"


class Transaction(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='transactions')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-transaction_date']

    def __str__(self):
        return f"Transaction - {self.employee.full_name} - {self.amount}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('salary_paid', 'Salary Paid'),
        ('salary_pending', 'Salary Pending'),
        ('payment_processed', 'Payment Processed'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee.full_name} - {self.title}"
