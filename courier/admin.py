"""
from django.contrib import admin
from .models import Customer, Booking, HeadOfficeReport, Expense, Invoice

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'account_type', 'default_rate')
    search_fields = ('name', 'phone')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'customer', 'date', 'account_type', 'amount', 'paid_amount', 'status')
    list_filter = ('date', 'account_type', 'status', 'amount_type')
    search_fields = ('tracking_id', 'customer__name', 'from_address__name', 'to_address__name')

@admin.register(HeadOfficeReport)
class HeadOfficeReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_booking', 'total_amount')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'amount')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_from', 'date_to', 'total_amount', 'paid')
"""

from django.contrib import admin

# Our MongoDB-backed classes are not Django models, so we cannot register them here.
# The Django admin will only show built-in auth models (User, Group) and allauth models.

# You can keep this file empty or use it to customize admin site title, etc.
admin.site.site_header = "Courier Manager Admin"
admin.site.site_title = "Courier Admin"
admin.site.index_title = "Welcome to Courier Admin"