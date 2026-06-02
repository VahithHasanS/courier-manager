from django import forms
from datetime import date

class BookingForm(forms.Form):
    date = forms.DateField(initial=date.today, widget=forms.DateInput(attrs={'type': 'date'}))
    customer_name = forms.CharField(max_length=100, required=False)
    # From address
    from_address_name = forms.CharField(max_length=100, label="From Name")
    from_address_address_line = forms.CharField(max_length=200, label="From Address")
    from_address_city = forms.CharField(max_length=100, label="From City")
    from_address_phone = forms.CharField(max_length=15, required=False, label="From Phone")
    # To address
    to_address_name = forms.CharField(max_length=100, label="To Name")
    to_address_address_line = forms.CharField(max_length=200, label="To Address")
    to_address_city = forms.CharField(max_length=100, label="To City")
    to_address_phone = forms.CharField(max_length=15, required=False, label="To Phone")

    weight = forms.FloatField(min_value=0)
    pieces = forms.IntegerField(min_value=0)
    tracking_id = forms.CharField(max_length=50)
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    amount_type = forms.ChoiceField(choices=[
        ('hand_cash', 'Hand Cash'), ('upi', 'UPI'), ('cheque', 'Cheque'),
        ('bank_transfer', 'Bank Transaction'), ('free', 'Free'), ('none', 'None'),
    ], initial='none')
    paid_amount = forms.DecimalField(max_digits=10, decimal_places=2, initial=0, required=False)
    remark = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}))
    image = forms.ImageField(required=False)
    account_type = forms.ChoiceField(choices=[('cash', 'Cash'), ('credit', 'Credit')], initial='cash')
    status = forms.ChoiceField(choices=[
        ('pending', 'Pending'), ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'), ('issue', 'Issue')
    ], initial='pending')
    complaint = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}))


class CustomerForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)
    email = forms.EmailField(required=False)
    account_type = forms.ChoiceField(choices=[('cash', 'Cash'), ('credit', 'Credit')], initial='cash')
    default_rate = forms.DecimalField(max_digits=10, decimal_places=2, initial=0)
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}))


class ExpenseForm(forms.Form):
    date = forms.DateField(initial=date.today, widget=forms.DateInput(attrs={'type': 'date'}))
    description = forms.CharField(max_length=200)
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    remark = forms.CharField(required=False)
    linked_booking_id = forms.CharField(max_length=50, required=False)


class HeadOfficeReportForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    total_booking = forms.IntegerField(min_value=0, initial=0)
    total_cash_booking = forms.IntegerField(min_value=0, initial=0)
    total_credit_booking = forms.IntegerField(min_value=0, initial=0)
    total_pieces = forms.IntegerField(min_value=0, initial=0)
    total_cash_pieces = forms.IntegerField(min_value=0, initial=0)
    total_credit_pieces = forms.IntegerField(min_value=0, initial=0)
    total_amount = forms.DecimalField(max_digits=12, decimal_places=2, initial=0)
    total_cash_amount = forms.DecimalField(max_digits=12, decimal_places=2, initial=0)
    total_credit_amount = forms.DecimalField(max_digits=12, decimal_places=2, initial=0)
    total_extra = forms.DecimalField(max_digits=10, decimal_places=2, initial=0)
    total_inverse = forms.DecimalField(max_digits=10, decimal_places=2, initial=0)
    remark = forms.CharField(required=False)