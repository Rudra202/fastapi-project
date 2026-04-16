from fastapi import FastAPI
from app.routers import auth, students, courses, enrollments

app = FastAPI(
    title="Course Enrollment API",
    description="FastAPI project with JWT auth, PostgreSQL, SQLAlchemy, Alembic, Docker",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(enrollments.router)


@app.get("/")
def root():
    return {"message": "Course Enrollment API is running"}