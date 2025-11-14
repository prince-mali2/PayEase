from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Public Home
    path('', views.home, name='home'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Employee Management
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employees/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    
    # Attendance
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/create/', views.attendance_create, name='attendance_create'),
    
    # Salary
    path('salaries/', views.salary_list, name='salary_list'),
    path('salaries/create/', views.salary_create, name='salary_create'),
    path('salaries/<int:pk>/', views.salary_detail, name='salary_detail'),
    path('salaries/<int:pk>/calculate/', views.salary_calculate, name='salary_calculate'),  # Accepts both GET and POST
    
    # Payment
    path('salaries/<int:salary_id>/payment/', views.payment_process, name='payment_process'),
    path('salaries/<int:salary_id>/mark-unpaid/', views.payment_mark_unpaid, name='payment_mark_unpaid'),
    
    # Transactions
    path('transactions/', views.transaction_history, name='transaction_history'),
    path('transactions/<int:employee_id>/', views.transaction_history, name='transaction_history_employee'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.notification_mark_read, name='notification_mark_read'),
]


