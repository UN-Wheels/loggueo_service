# app/db/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False, default="estudiante")
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    major = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    rating = Column(Float, default=0.0, nullable=True)
    vehicles = relationship(
        "Vehicle", back_populates="owner", cascade="all, delete-orphan"
    )


class UserLog(Base):
    __tablename__ = "user_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    login_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    token = Column(String, nullable=False)


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    plate = Column(String, unique=True, index=True, nullable=False)
    vehicle_type = Column(String, nullable=False)
    brand = Column(String, nullable=True)
    model = Column(String, nullable=True)
    color = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)

    owner = relationship("User", back_populates="vehicles")
