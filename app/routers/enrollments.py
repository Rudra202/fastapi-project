from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.course import Course
from app.schemas.enrollment import EnrollmentCreate, EnrollmentOut
from app.core.security import get_current_user, require_admin

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.post("/", response_model=EnrollmentOut, status_code=status.HTTP_201_CREATED)
def create_enrollment(
    enrollment_data: EnrollmentCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin),
):
    student = db.query(Student).filter(Student.id == enrollment_data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    course = db.query(Course).filter(Course.id == enrollment_data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    existing = db.query(Enrollment).filter(
        Enrollment.student_id == enrollment_data.student_id,
        Enrollment.course_id == enrollment_data.course_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Student already enrolled in this course")

    enrollment = Enrollment(**enrollment_data.model_dump())
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.get("/", response_model=list[EnrollmentOut])
def list_enrollments(
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return db.query(Enrollment).all()


@router.get("/{enrollment_id}", response_model=EnrollmentOut)
def get_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin),
):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    db.delete(enrollment)
    db.commit()