# 🚀 Course Enrollment API (FastAPI)

A fully functional backend API built using **FastAPI**, **PostgreSQL**, and **JWT Authentication**.  
This project demonstrates real-world backend development with proper structure, authentication, and database integration.

---

## 📌 Features

- 🔐 User Registration & Login (JWT Auth)
- 👨‍🎓 Student Management (CRUD)
- 📚 Course Management (CRUD)
- 📝 Enrollment System
- 🔎 Search & Filter
- 📄 Pagination
- 🛡 Role-based Access (Admin / Student)
- 🗄 PostgreSQL Database
- 🔄 Alembic Migrations
- 📑 Swagger API Docs

---

## 🛠 Tech Stack

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Alembic**
- **JWT (python-jose)**
- **Pydantic**
- **Uvicorn**

---

## 📂 Project Structure
app/
│
├── main.py
├── core/
│ ├── config.py
│ └── security.py
├── db/
│ └── database.py
├── models/
├── schemas/
├── routers/
└── ...



---

## ⚙️ Setup Instructions (Local)

### 1️⃣ Clone the repo

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

### 2️⃣ Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

###3️⃣ Install dependencies
pip install -r requirements.txt


4️⃣ Setup environment variables
Create a .env file:

DATABASE_URL=postgresql://localhost:5432/course_enrollment
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

5️⃣ Run migrations
alembic upgrade head

6️⃣ Start server
uvicorn app.main:app --reload

7️⃣ Open API Docs
http://127.0.0.1:8000/docs



🌐 Live Demo
👉 https://fastapi-project-y5hx.onrender.com/docs

🔑 Authentication Flow
Register user → /auth/register

Login → /auth/login

Get JWT token

Click Authorize in Swagger

Use API endpoints

📡 API Endpoints
Auth
POST /auth/register

POST /auth/login

Students
GET /students

POST /students

PUT /students/{id}

DELETE /students/{id}

Courses
GET /courses

POST /courses

PUT /courses/{id}

DELETE /courses/{id}

Enrollments
POST /enrollments

GET /enrollments

DELETE /enrollments/{id}

⚠️ Common Issues
❌ 500 Error → Run migrations

❌ DB connection error → Check DATABASE_URL

❌ Auth error → Check JWT token
