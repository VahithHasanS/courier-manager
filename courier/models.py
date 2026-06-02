import uuid
from datetime import date, datetime
from .mongo import CustomerManager, BookingManager, HOManager, ExpenseManager, InvoiceManager, TrackingHistoryManager

# ---------- Tracking History ----------
class TrackingHistory:
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.tracking_id = kwargs.get('tracking_id')
        self.status = kwargs.get('status')
        self.timestamp = kwargs.get('timestamp', datetime.now())
        if isinstance(self.timestamp, str):
            try:
                self.timestamp = datetime.fromisoformat(self.timestamp)
            except ValueError:
                self.timestamp = datetime.now()
        self.remark = kwargs.get('remark', '')
        self.updated_by = kwargs.get('updated_by', 'System')

    def save(self):
        data = {
            'tracking_id': self.tracking_id,
            'status': self.status,
            'timestamp': self.timestamp.isoformat() if hasattr(self.timestamp, 'isoformat') else str(self.timestamp),
            'remark': self.remark,
            'updated_by': self.updated_by,
        }
        if not self._id:
            self._id = TrackingHistoryManager.create(data)

    @staticmethod
    def get_history(tracking_id):
        return [TrackingHistory(**h) for h in TrackingHistoryManager.get_by_tracking_id(tracking_id)]

# ---------- Customer ----------
class Customer:
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')          # MongoDB ObjectId
        self.name = kwargs.get('name', '')
        self.phone = kwargs.get('phone', '')
        self.email = kwargs.get('email', '')
        self.account_type = kwargs.get('account_type', 'cash')  # 'cash' or 'credit'
        self.default_rate = kwargs.get('default_rate', 0.0)      # per kg per piece
        self.address = kwargs.get('address', '')

    def save(self):
        data = {
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'account_type': self.account_type,
            'default_rate': self.default_rate,
            'address': self.address,
        }
        if self._id:
            CustomerManager.update(self._id, data)
        else:
            self._id = CustomerManager.create(data)

    def delete(self):
        if self._id:
            CustomerManager.delete(self._id)

    @staticmethod
    def get_all():
        return [Customer(**c) for c in CustomerManager.all()]

    @staticmethod
    def get(id):
        data = CustomerManager.get(id)
        return Customer(**data) if data else None

    @staticmethod
    def get_or_create(name, defaults=None):
        # search by name
        for c in CustomerManager.all():
            if c['name'] == name:
                return Customer(**c)
        # create new
        cust = Customer(name=name, **(defaults or {}))
        cust.save()
        return cust

# ---------- Address (embedded) ----------
class Address:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.address_line = kwargs.get('address_line', '')
        self.city = kwargs.get('city', '')
        self.phone = kwargs.get('phone', '')

    def to_dict(self):
        return {
            'name': self.name,
            'address_line': self.address_line,
            'city': self.city,
            'phone': self.phone,
        }

    @staticmethod
    def from_dict(d):
        return Address(**d)

# ---------- Booking ----------
class Booking:
    STATUS_CHOICES = ['pending', 'in_transit', 'delivered', 'issue']
    AMOUNT_TYPE_CHOICES = ['hand_cash', 'upi', 'cheque', 'bank_transfer', 'free', 'none']

    def __init__(self, **kwargs):
        
        self._id = kwargs.get('_id')
        self.date = kwargs.get('date', date.today())
        if isinstance(self.date, str):
            self.date = datetime.strptime(self.date, '%Y-%m-%d').date()
        self.customer_id = kwargs.get('customer_id')          # customer name or id reference
        self.customer_name = kwargs.get('customer_name', '')
        self.from_address = Address(**kwargs['from_address']) if 'from_address' in kwargs and isinstance(kwargs['from_address'], dict) else kwargs.get('from_address', Address())
        self.to_address = Address(**kwargs['to_address']) if 'to_address' in kwargs and isinstance(kwargs['to_address'], dict) else kwargs.get('to_address', Address())
        self.weight = kwargs.get('weight', 0.0)
        self.pieces = kwargs.get('pieces', 0)
        self.tracking_id = kwargs.get('tracking_id', str(uuid.uuid4().hex[:10].upper()))
        self.amount = float(kwargs.get('amount', 0))
        self.amount_type = kwargs.get('amount_type', 'none')
        self.paid_amount = float(kwargs.get('paid_amount', 0))
        self.extra = float(kwargs.get('extra', 0))
        self.inverse = float(kwargs.get('inverse', 0))
        self.remark = kwargs.get('remark', '')
        self.image = kwargs.get('image', None)                # filename or path
        self.account_type = kwargs.get('account_type', 'cash')
        self.status = kwargs.get('status', 'pending')
        self.complaint = kwargs.get('complaint', '')
        self.barcode_image = kwargs.get('barcode_image', None)
    
    
    @property
    def whatsapp_share_url(self):
        phone = self.to_address.phone if self.to_address else ''
        # Remove everything except digits
        cleaned = ''.join(filter(str.isdigit, phone))
        if not cleaned:
            return None
        # Build the message (you can customise this)
        lines = [
            f"Hello {self.to_address.name},",
            f"Your courier tracking ID: {self.tracking_id}",
            f"Status: {self.status.upper()}",
            f"Date: {self.date}",
            f"From: {self.from_address.name}, {self.from_address.city}",
            f"To: {self.to_address.name}, {self.to_address.city}",
            f"Amount: ₹{self.amount}",
            f"Paid: ₹{self.paid_amount}",
        ]
        if self.remark:
            lines.append(f"Remark: {self.remark}")
        lines.append("Thank you for using our courier service!")
        message = "\n".join(lines)
        import urllib.parse
        encoded = urllib.parse.quote(message)
        return f"https://wa.me/{cleaned}?text={encoded}"
    
    @property
    def pk(self):
        return str(self._id) if self._id else ''
    
    @property
    def amount_type_display(self):
        # Convert 'hand_cash' → 'Hand Cash', 'bank_transfer' → 'Bank Transfer', etc.
        return self.amount_type.replace('_', ' ').title()

    def save(self):
        # calculate extra/inverse
        self.extra = 0
        self.inverse = 0
        if self.paid_amount > self.amount:
            self.extra = self.paid_amount - self.amount
        elif self.paid_amount < self.amount:
            self.inverse = self.amount - self.paid_amount

        data = {
            'date': self.date.isoformat() if hasattr(self.date, 'isoformat') else str(self.date),
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'from_address': self.from_address.to_dict() if hasattr(self.from_address, 'to_dict') else self.from_address,
            'to_address': self.to_address.to_dict() if hasattr(self.to_address, 'to_dict') else self.to_address,
            'weight': self.weight,
            'pieces': self.pieces,
            'tracking_id': self.tracking_id,
            'amount': self.amount,
            'amount_type': self.amount_type,
            'paid_amount': self.paid_amount,
            'extra': self.extra,
            'inverse': self.inverse,
            'remark': self.remark,
            'image': self.image,
            'account_type': self.account_type,
            'status': self.status,
            'complaint': self.complaint,
            'barcode_image': self.barcode_image,
        }
        if self._id:
            BookingManager.update(self._id, data)
        else:
            self._id = BookingManager.create(data)

    def delete(self):
        if self._id:
            BookingManager.delete(self._id)

    @staticmethod
    def get_all():
        bookings = []
        for b in BookingManager.all():
            bookings.append(Booking(**b))
        return bookings

    @staticmethod
    def get(id):
        data = BookingManager.get(id)
        return Booking(**data) if data else None

    @staticmethod
    def filter(**kwargs):
        # Convert kwargs to MongoDB query (simple version)
        query = {}
        for key, value in kwargs.items():
            if value:
                if key == 'date__gte':
                    query['date'] = {**query.get('date', {}), '$gte': value.isoformat() if hasattr(value, 'isoformat') else str(value)}
                elif key == 'date__lte':
                    query['date'] = {**query.get('date', {}), '$lte': value.isoformat() if hasattr(value, 'isoformat') else str(value)}
                elif key == 'customer_name__icontains':
                    query['customer_name'] = {'$regex': value, '$options': 'i'}
                elif key == 'tracking_id__icontains':
                    query['tracking_id'] = {'$regex': value, '$options': 'i'}
                elif key == 'status':
                    query['status'] = value
                elif key == 'account_type':
                    query['account_type'] = value
                else:
                    query[key] = value
        results = BookingManager.filter(query)
        return [Booking(**b) for b in results]

# ---------- HeadOfficeReport ----------
class HeadOfficeReport:
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.date = kwargs.get('date', date.today())
        if isinstance(self.date, str):
            self.date = datetime.strptime(self.date, '%Y-%m-%d').date()
        self.total_booking = kwargs.get('total_booking', 0)
        self.total_cash_booking = kwargs.get('total_cash_booking', 0)
        self.total_credit_booking = kwargs.get('total_credit_booking', 0)
        self.total_pieces = kwargs.get('total_pieces', 0)
        self.total_cash_pieces = kwargs.get('total_cash_pieces', 0)
        self.total_credit_pieces = kwargs.get('total_credit_pieces', 0)
        self.total_amount = float(kwargs.get('total_amount', 0))
        self.total_cash_amount = float(kwargs.get('total_cash_amount', 0))
        self.total_credit_amount = float(kwargs.get('total_credit_amount', 0))
        self.total_extra = float(kwargs.get('total_extra', 0))
        self.total_inverse = float(kwargs.get('total_inverse', 0))
        self.remark = kwargs.get('remark', '')

    @property
    def pk(self):
        return str(self._id) if self._id else ''

    def save(self):
        data = {
            'date': self.date.isoformat() if hasattr(self.date, 'isoformat') else str(self.date),
            'total_booking': self.total_booking,
            'total_cash_booking': self.total_cash_booking,
            'total_credit_booking': self.total_credit_booking,
            'total_pieces': self.total_pieces,
            'total_cash_pieces': self.total_cash_pieces,
            'total_credit_pieces': self.total_credit_pieces,
            'total_amount': self.total_amount,
            'total_cash_amount': self.total_cash_amount,
            'total_credit_amount': self.total_credit_amount,
            'total_extra': self.total_extra,
            'total_inverse': self.total_inverse,
            'remark': self.remark,
        }
        if self._id:
            HOManager.update(self._id, data)
        else:
            self._id = HOManager.create(data)

    @staticmethod
    def get_all():
        return [HeadOfficeReport(**r) for r in HOManager.all()]

# ---------- Expense ----------
class Expense:
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.date = kwargs.get('date', date.today())
        if isinstance(self.date, str):
            self.date = datetime.strptime(self.date, '%Y-%m-%d').date()
        self.description = kwargs.get('description', '')
        self.amount = float(kwargs.get('amount', 0))
        self.remark = kwargs.get('remark', '')
        self.linked_booking_id = kwargs.get('linked_booking_id')   # tracking_id or _id
    
    @property
    def pk(self):
        return str(self._id) if self._id else ''

    def save(self):
        data = {
            'date': self.date.isoformat() if hasattr(self.date, 'isoformat') else str(self.date),
            'description': self.description,
            'amount': self.amount,
            'remark': self.remark,
            'linked_booking_id': self.linked_booking_id,
        }
        if self._id:
            ExpenseManager.update(self._id, data)
        else:
            self._id = ExpenseManager.create(data)

    @staticmethod
    def get_all():
        return [Expense(**e) for e in ExpenseManager.all()]

# ---------- Invoice ----------
class Invoice:
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.customer_name = kwargs.get('customer_name', '')
        self.date_from = kwargs.get('date_from', '')
        self.date_to = kwargs.get('date_to', '')
        self.created_at = kwargs.get('created_at', datetime.now())
        self.total_amount = float(kwargs.get('total_amount', 0))
        self.booking_ids = kwargs.get('booking_ids', [])   # list of tracking_ids
        self.paid = kwargs.get('paid', False)

    @property
    def pk(self):
        return str(self._id) if self._id else ''

    def save(self):
        data = {
            'customer_name': self.customer_name,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'created_at': self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else str(self.created_at),
            'total_amount': self.total_amount,
            'booking_ids': self.booking_ids,
            'paid': self.paid,
        }
        if self._id:
            InvoiceManager.update(self._id, data)
        else:
            self._id = InvoiceManager.create(data)

    @staticmethod
    def get_all():
        return [Invoice(**i) for i in InvoiceManager.all()]

    @staticmethod
    def get(id):
        data = InvoiceManager.get(id)
        return Invoice(**data) if data else None