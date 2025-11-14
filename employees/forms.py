from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import User, Employee, Attendance, Salary, Payment


class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'role', 'password1', 'password2']


class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # For editing, include the current user if linked
        if self.instance and self.instance.pk and self.instance.user:
            current_user = self.instance.user
            queryset = User.objects.filter(
                models.Q(role='employee', employee_profile__isnull=True) | 
                models.Q(pk=current_user.pk)
            )
        else:
            queryset = User.objects.filter(role='employee', employee_profile__isnull=True)
        
        self.fields['user'] = forms.ModelChoiceField(
            queryset=queryset,
            required=False,
            empty_label="-- Select User Account (Optional) --",
            help_text="Link this employee to an existing user account",
            widget=forms.Select(attrs={'class': 'form-select'})
        )
    
    class Meta:
        model = Employee
        fields = [
            'user', 'employee_id', 'full_name', 'email', 'phone', 'address',
            'date_of_joining', 'designation', 'department',
            'bank_name', 'account_number', 'ifsc_code', 'base_salary'
        ]
        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'status', 'check_in', 'check_out', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'check_in': forms.TimeInput(attrs={'type': 'time'}),
            'check_out': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'employee': forms.Select(attrs={'class': 'form-select'}),
        }


class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = [
            'employee', 'month', 'year', 'base_salary',
            'total_working_days', 'days_present', 'days_absent',
            'days_on_leave', 'half_days',
            'allowances', 'deductions'
        ]
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_date', 'payment_method', 'transaction_id', 'notes']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

