from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Admin(Base):
    __tablename__ = "admin"

    adminId = Column(Integer, primary_key=True, index=True)
    adminUsername = Column(String(255), unique=True, nullable=False)
    adminName = Column(String(100), unique=True, nullable=False)
    adminContactNo = Column(String(15), unique=True, nullable=False)
    adminPosition = Column(String(50), unique=False, nullable=False)
    adminUnit = Column(String(30), unique=False, nullable=False)
    adminPassword = Column(String(255), nullable=False)
