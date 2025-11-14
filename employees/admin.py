from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Employee, Attendance, Salary, Payment, Transaction, Notification

# Admin site branding
admin.site.site_header = "PayEase Admin"
admin.site.site_title = "PayEase Admin"
admin.site.index_title = "Welcome to PayEase Administration"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_staff', 'is_superuser']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone')}),
    )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'email', 'department', 'base_salary', 'is_active']
    list_filter = ['department', 'is_active', 'date_of_joining']
    search_fields = ['employee_id', 'full_name', 'email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status', 'check_in', 'check_out']
    list_filter = ['status', 'date']
    search_fields = ['employee__full_name', 'employee__employee_id']
    date_hierarchy = 'date'


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ['employee', 'month', 'year', 'net_salary', 'is_paid']
    list_filter = ['is_paid', 'year', 'month']
    search_fields = ['employee__full_name', 'employee__employee_id']
    readonly_fields = ['calculated_amount', 'net_salary', 'created_at', 'updated_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['salary', 'payment_date', 'payment_method', 'processed_by']
    list_filter = ['payment_method', 'payment_date']
    search_fields = ['salary__employee__full_name', 'transaction_id']
    date_hierarchy = 'payment_date'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['employee', 'amount', 'transaction_date', 'payment']
    list_filter = ['transaction_date']
    search_fields = ['employee__full_name', 'description']
    date_hierarchy = 'transaction_date'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['employee', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['employee__full_name', 'title', 'message']
    readonly_fields = ['created_at']
