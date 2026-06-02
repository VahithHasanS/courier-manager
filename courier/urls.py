from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Bookings
    path('booking/add/', views.add_booking, name='add_booking'),
    path('booking/<str:pk>/edit/', views.edit_booking, name='edit_booking'),
    path('booking/list/', views.booking_list, name='booking_list'),
    path('booking/<str:pk>/status/', views.update_status, name='update_status'),
    path('booking/<str:pk>/', views.booking_detail, name='booking_detail'),
    
    # Head Office Reports
    path('ho-report/add/', views.add_ho_report, name='add_ho_report'),
    path('ho-report/list/', views.ho_report_list, name='ho_report_list'),
    
    # Search
    path('search/', views.search_view, name='search'),
    
    # Invoices
    path('invoice/create/', views.create_invoice, name='create_invoice'),
    path('invoice/list/', views.invoice_list, name='invoice_list'),
    path('invoice/<str:pk>/', views.invoice_detail, name='invoice_detail'),
    
    # Export / Import
    path('export/<str:model>/', views.export_excel, name='export_excel'),
    path('import/<str:model>/', views.import_excel, name='import_excel'),
    
    # Expense
    path('expense/add/', views.add_expense, name='add_expense'),
    path('expense/list/', views.expense_list, name='expense_list'),
    
    # Backup (simple JSON download)
    path('backup/', views.backup_data, name='backup'),
    path('api/bookings/', views.api_bookings, name='api_bookings'),
    
    # Public Tracking
    path('track/', views.track_package, name='track_package'),

    path('analytics/', views.analytics, name='analytics'),
]