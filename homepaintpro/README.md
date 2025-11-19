# HomePaintPro
HomePaintPro – Painter Service Management System (Flask App) A complete service booking and job management system built using Flask, SQLite, and Bootstrap, designed for painting businesses. Clients can request painting services, admins can manage bookings, and painters get their own login to view assigned tasks and update work status.
# 🎨 HomePaintPro — Painter Service Management System (Flask)

HomePaintPro is a complete painter service booking and job management system built using **Flask, SQLite, and Bootstrap**.

It helps painting businesses manage client bookings, assign painters to jobs, and track progress. Clients can request painting services online, while admin manages operations, and painters have their own login to view assigned tasks and update status.

---

## 🚀 Features

### 🧾 Client Portal
- Book painting services online
- Enter area size, paint type, wall condition, room count, budget, etc.
- Automatic cost estimation before booking

### 🛠 Admin Dashboard
- View all client bookings
- Assign painters manually
- Update status, rate & job notes
- Manage painter accounts (Add / Activate / Deactivate)

### 👷 Painter Panel
- Login using phone + password
- View only assigned tasks
- Update work status (Pending → In Progress → Completed)

### 🗄 Database Design
- SQLite + SQLAlchemy ORM
- Tables: `AdminUser`, `Painter`, `ClientBooking`

---

## 🧪 Tech Stack

| Component | Technology |
|----------|------------|
| Backend | Python, Flask |
| Frontend | Bootstrap 5, HTML, Jinja2 |
| DB | SQLite + SQLAlchemy |
| Deployment | PythonAnywhere / Render / Localhost |

---

## 📂 Project Structure

