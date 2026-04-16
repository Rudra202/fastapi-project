from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate, StudentOut
from app.core.security import get_current_user, require_admin

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin),
):
    existing = db.query(Student).filter(Student.email == student_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student email already exists")

    student = Student(**student_data.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.get("/", response_model=list[StudentOut])
def list_students(
    skip: int = 0,
    limit: int = Query(default=10, le=100),
    search: str | None = None,
    department: str | None = None,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    query = db.query(Student)

    if search:
        query = query.filter(Student.full_name.ilike(f"%{search}%"))

    if department:
        query = query.filter(Student.department.ilike(f"%{department}%"))

    students = query.offset(skip).limit(limit).all()
    return students


@router.get("/{student_id}", response_model=StudentOut)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=StudentOut)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    email_owner = db.query(Student).filter(
        Student.email == student_data.email,
        Student.id != student_id
    ).first()
    if email_owner:
        raise HTTPException(status_code=400, detail="Email already in use")

    for key, value in student_data.model_dump().items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()