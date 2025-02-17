# **Expense Tracker 💰📊**
A **full-stack** Expense Tracker app built with **Django REST Framework** (Backend) and **React.js** (Frontend). It allows users to **track expenses, generate reports**, and **export data in CSV/PDF/Excel** formats.

---

## 🚀 **Features**
✅ **User Authentication** – Signup, Login, JWT Token-based Authentication  
✅ **Expense Management** – Add, Edit, Delete, List expenses  
✅ **Monthly Reports** – Generate category-wise expense summary  
✅ **Export Reports** – Download reports in **CSV, PDF, and Excel**  
✅ **Performance Optimization** – **Caching frequently accessed reports**  
✅ **Admin Dashboard** – View all users (Admin only)  

---

## 🛠 **Tech Stack**
### **Backend**
- 🐍 **Django Rest Framework** – API development
- 🗄 **SQLite** – Database
- 🔄 **LocMemCache** – Caching reports for performance


### **Frontend**
- ⚛ **React.js** – UI Development
- 🎨 **Material UI** – Styling

---

## 📌 **Installation & Setup**
### **1️⃣ Clone the Repo**
```bash
git clone https://github.com/your-repo/expense-tracker.git
cd expense-tracker
```

### **2️⃣ Backend Setup (Django)**
```bash
cd backend
python -m venv expense-tracker-env  # Create Virtual Environment
source expense-tracker-env/bin/activate  # Activate (For Mac/Linux)
expense-tracker-env\Scripts\activate  # Activate (For Windows)
pip install -r requirements.txt  # Install dependencies
python manage.py migrate  # Apply migrations
python manage.py createsuperuser  # Create admin user
python manage.py runserver  # Start server
```

### **3️⃣ Frontend Setup (React)**
```bash
cd frontend
npm install  # Install dependencies
npm start  # Start React app
```
The frontend will run at **http://localhost:3000**  
The backend API will run at **http://127.0.0.1:8000**

---

## 📡 **API Endpoints**
| **Method** | **Endpoint** | **Description** |
|-----------|-------------|----------------|
| `POST` | `/api/register/` | Register a new user |
| `POST` | `/api/login/` | User login (JWT Auth) |
| `POST` | `/api/token/refresh/` | Refresh JWT Token |
| `GET` | `/api/expenses/list/` | List all user expenses |
| `POST` | `/api/expenses/create/` | Create a new expense |
| `DELETE` | `/api/expenses/{id}/delete/` | Delete an expense |
| `PUT` | `/api/expenses/{id}/update/` | Edit an expense |
| `GET` | `/api/report/monthly/?month=YYYY-MM` | Get monthly report |
| `GET` | `/api/report/download/csv/` | Export CSV |
| `GET` | `/api/report/download/pdf/` | Export PDF |
| `GET` | `/api/report/download/excel/` | Export Excel |

---

**4️⃣ Restart Django Server**
```bash
python manage.py runserver
```

---

## 🎯 **Contributing**
nischalare

## 📩 **Contact**
https://github.com/nischalare 



