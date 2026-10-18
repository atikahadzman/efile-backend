from sqlalchemy.orm import Session
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate
from app.core.security import hash_password


def fetch_all_admins(db: Session):
    return db.query(Admin).all()


def fetch_admin_by_id(db: Session, adminId: int):
    return (
        db.query(Admin)
        .filter(Admin.adminId == adminId)
        .first()
    )


def create_admin(db: Session, admin_data: AdminCreate):
    data = admin_data.model_dump()

    hashed_password = hash_password(data.pop("adminPassword"))

    admin = Admin(
        adminName=data["adminName"],
        adminUsername=data["adminUsername"],
        adminContactNo=data["adminContactNo"],
        adminPosition=data["adminPosition"],
        adminUnit=data["adminUnit"],
        adminPassword=hashed_password
    )

    try:
        db.add(admin)
        db.commit()
        db.refresh(admin)
        return admin
    except Exception:
        db.rollback()
        raise


def update_admin(
    db: Session,
    adminId: int,
    admin_data: AdminUpdate
):
    admin = fetch_admin_by_id(db, adminId)

    if admin is None:
        return None

    update_data = admin_data.model_dump(exclude_unset=True)

    if update_data.get("adminPassword"):
        update_data["adminPassword"] = hash_password(
            update_data["adminPassword"]
        )

    for field, value in update_data.items():
        setattr(admin, field, value)

    db.commit()
    db.refresh(admin)

    return admin


def delete_admin(db: Session, adminId: int):
    admin = fetch_admin_by_id(db, adminId)

    if admin is None:
        return None

    db.delete(admin)
    db.commit()

    return admin