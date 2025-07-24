# 🧳 Django Travel Booking App

A full-featured travel booking web application built with Django and MySQL. Users can register, log in, browse travel options (bus, train, flight), make bookings, cancel them, and manage their profiles.

🔗 **Live Demo (optional)**: _Add link if deployed_

## 🚀 Features

- User registration & login
- List of travel options with filter (type, source, destination, date)
- Book travel tickets (bus/train/flight)
- Cancel bookings
- View past and upcoming bookings
- Admin can add travel options via Django Admin
- Profile update with username & password change

## 🛠️ Tech Stack

- **Backend**: Django, MySQL
- **Frontend**: HTML, Bootstrap 5
- **Database**: MySQL
- **Auth**: Django's built-in authentication system

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Aman235-code/django-travel-booking-app.git
cd django-travel-booking-app
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create `.env` File for DB Credentials (🔐 Environment Variables (.env))

Create a `.env` file in the project root (where `manage.py` is located) with the following content:

```
DB_NAME=travel_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

> 💡 Make sure to replace `your_mysql_password` with your actual MySQL root password.

---

## 🧱 Database Setup (MySQL)

### 1. Create the database

Log into your MySQL CLI or GUI and run:

```sql
CREATE DATABASE travel_db;
```

### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🧪 Run the Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

---

## 🧑‍💻 Superuser (for Admin Panel)

```bash
python manage.py createsuperuser
```

Then log in at: `http://127.0.0.1:8000/admin`


## 📝 Folder Structure

```
travelbooking/
│
├── core/                # App logic
├── travelbooking/       # Project settings
├── manage.py
├── requirements.txt
├── .env
├── README.md
└── .gitignore
```

---

## 📸 Screenshots

_Add screenshots of key pages like Travel List, Booking Page, Profile Update, etc._

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 👤 Author

- GitHub: [Aman235-code](https://github.com/Aman235-code)
