from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate, CourseOut
from app.core.security import get_current_user, require_admin

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post("/", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin),
):
    existing = db.query(Course).filter(Course.code == course_data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Course code already exists")

    course = Course(**course_data.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.get("/", response_model=list[CourseOut])
def list_courses(
    skip: int = 0,
    limit: int = Query(default=10, le=100),
    search: str | None = None,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    query = db.query(Course)

    if search:
        query = query.filter(Course.title.ilike(f"%{search}%"))

    return query.offset(skip).limit(limit).all()


@router.get("/{course_id}", response_model=CourseOut)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.put("/{course_id}", response_model=CourseOut)
def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin),
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    code_owner = db.query(Course).filter(
        Course.code == course_data.code,
        Course.id != course_id
    ).first()
    if code_owner:
        raise HTTPException(status_code=400, detail="Course code already exists")

    for key, value in course_data.model_dump().items():
        setattr(course, key, value)

    db.commit()
    db.refresh(course)
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin),
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(course)
    db.commit()