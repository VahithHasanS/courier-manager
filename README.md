# Courier Manager

A full‑stack web application for courier branch managers to manage bookings, customers, expenses, invoices, head office reports, and more – all built with **Django** and **MongoDB**.

## Features

- 🔐 Secure login with session & Google authentication
- 📦 Booking management with auto‑calculation of extra/inverse amounts
- 📊 Smart dashboard with charts & progress bars
- 🔍 Search and filter bookings by any field
- 📋 Status tracking & complaint management
- 🧾 Invoice generation (printable & shareable)
- 📥 Excel import/export for bookings, reports, invoices
- 💰 Expense tracking with profit/loss analytics
- 🖼️ Bill image upload & view
- 📱 Responsive UI (mobile + desktop)
- 🔄 Backup data as JSON
- 💬 Send booking status to customers via WhatsApp

## Tech Stack

- **Backend:** Django (Python)  
- **Database:** MongoDB (via PyMongo), SQLite for user auth  
- **Frontend:** Bootstrap 5, Chart.js, Font Awesome  
- **Authentication:** django-allauth (Google OAuth support)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/courier-manager.git
   cd courier-manager
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
4. **Set up environment variables**
    Create a .env file in the project root.
    Add these lines (replace values):

    ```bash
    SECRET_KEY=your-secret-key-here
    DEBUG=True
    MONGO_URI=mongodb://localhost:27017
    MONGO_DB_NAME=courier_db
    ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create admin user**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run server**
   ```bash
   python manage.py runserver
   ```

8. **Run MongoDB**
   ```bash
   mongod
   ```
9. **Access the app**
   ```bash
   http://[IP_ADDRESS]/dashboard/
   ```

## Project Structure

```
courier-manager/
├── courier/
│   ├── migrations/
│   ├── templates/
│   │   ├── courier/
│   │   │   ├── base.html          # Master template
│   │   │   ├── index.html         # Dashboard
│   │   │   ├── booking_list.html  # Bookings table
│   │   │   ├── booking_detail.html  # Single booking view
│   │   │   ├── new_booking.html   # Create booking form
│   │   │   ├── customer_list.html
│   │   │   ├── customer_form.html
│   │   │   ├── invoice_list.html
│   │   │   ├── expense_form.html
│   │   │   ├── ho_report.html     # Head Office Report
│   │   │   ├── bill_entry.html
│   │   │   ├── search.html
│   │   │   └── 404.html
│   │   └── allauth/             # Allauth templates
│   ├── views.py                # All core views
│   ├── urls.py                 # App URLs
│   ├── models.py
│   ├── utils.py                # Helper utilities
│   └── tests.py
├── courier_project/
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Project URLs
│   └── asgi.py / wsgi.py
├── templates/                  # Global templates
├── static/
├── media/
├── .env                      # Environment variables
├── requirements.txt
├── manage.py
└── README.md
```


## Features

- 🔐 Secure login with session & Google authentication
- 📦 Booking management with auto‑calculation of extra/inverse amounts
- 📊 Smart dashboard with charts & progress bars
- 🔍 Search and filter bookings by any field
- 📋 Status tracking & complaint management
- 🧾 Invoice generation (printable & shareable)
- 📥 Excel import/export for bookings, reports, invoices
- 💰 Expense tracking with profit/loss analytics
- 🖼️ Bill image upload & view
- 📱 Responsive UI (mobile + desktop)
- 🔄 Backup data as JSON
- 💬 Send booking status to customers via WhatsApp

## Tech Stack

- **Backend:** Django (Python)  
- **Database:** MongoDB (via PyMongo), SQLite for user auth  
- **Frontend:** Bootstrap 5, Chart.js, Font Awesome  
- **Authentication:** django-allauth (Google OAuth support)

## Deployment

To deploy this application on a server, you can use a combination of:

1. **Gunicorn:** Python WSGI HTTP Server
2. **Nginx:** Reverse Proxy
3. **Systemd:** Process Management

### Quick Deployment Steps

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Create Systemd Service**
   Create `/etc/systemd/system/courier.service`:
   ```ini
   [Unit]
   Description=Courier Manager
   After=network.target

   [Service]
   User=youruser
   Group=www-data
   WorkingDirectory=/path/to/your/project
   Environment="PATH=/path/to/venv/bin"
   ExecStart=/path/to/venv/bin/gunicorn courier_project.wsgi:application --bind [IP_ADDRESS]:8000

   [Install]
   WantedBy=multi-user.target
   ```

3. **Configure Nginx**
   Create `/etc/nginx/sites-available/courier`:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location /static/ {
           alias /path/to/your/project/static/;
       }

       location /media/ {
           alias /path/to/your/project/media/;
       }

       location / {
           proxy_pass http://[IP_ADDRESS];
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```
   Enable the site:
   ```bash
   ln -s /etc/nginx/sites-available/courier /etc/nginx/sites-enabled/
   nginx -t
   systemctl reload nginx
   ```

4. **Start Services**
   ```bash
   systemctl start courier
   systemctl enable courier
   ```

## Database

The application uses MongoDB for core data and SQLite for authentication. Ensure MongoDB is running and accessible.

## Usage

- Login with superuser or sign up.
- Add bookings, generate invoices, track expenses.
- View analytics for business insights.
- Share booking details directly via WhatsApp.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

> **Note:** Replace `yourusername` in the clone URL with your actual GitHub username.

## Acknowledgments

- Thanks to Django community for the amazing framework.
- Thanks to MongoDB for the NoSQL database.
- Thanks to Bootstrap for the frontend styling.

## Contact

For any issues or questions, please contact vahithhasans@gmail.com
