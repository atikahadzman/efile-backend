import logging
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.database import get_db
from app.schemas.admin import AdminCreate, AdminUpdate, AdminResponse
from app.services import admin as admin_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("db_logger")

router = APIRouter(
    prefix="/admins",
    tags=["Admins"]
)

# get all admin
@router.get("", response_model=list[AdminResponse])
def get_all_admins(db: Session = Depends(get_db)):
    return admin_service.fetch_all_admins(db)


# get admin by adminId
@router.get("/{adminId}", response_model=AdminResponse)
def get_admin_by_id(
    adminId: int,
    db: Session = Depends(get_db)
):
    admin_record = admin_service.fetch_admin_by_id(db, adminId)

    if admin_record is None:
        raise HTTPException(
            status_code=404,
            detail="Admin record not found"
        )

    return admin_record


# create admin
@router.post(
    "",
    response_model=AdminResponse,
    status_code=status.HTTP_201_CREATED
)
def create_admin(
    admin_data: AdminCreate,
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"HERE: {admin_data.model_dump_json()}")
        return admin_service.create_admin(db, admin_data)
    except IntegrityError as e:
        db.rollback()
        logger.exception(
            "Admin creation failed due to a database integrity error"
        )

        logger.error("Database error: %s", e.orig)

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admin creation failed due to a duplicate or invalid database value"
        )


# update admin
@router.put("/{adminId}", response_model=AdminResponse)
def update_admin(
    adminId: int,
    admin_data: AdminUpdate,
    db: Session = Depends(get_db)
):
    try:
        admin = admin_service.update_admin(
            db, adminId, admin_data
        )

        if admin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin record not found"
            )

        return admin

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admin update failed due to a duplicate or invalid database value"
        )


# delete admin
@router.delete("/{adminId}")
def delete_admin(
    adminId: int,
    db: Session = Depends(get_db)
):
    admin = admin_service.delete_admin(db, adminId)

    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin record not found"
        )

    return {
        "message": "Admin deleted successfully",
        "adminId": adminId
    }