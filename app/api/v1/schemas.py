# app/api/v1/schemas.py
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Schema para crear un usuario"""

    name: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    major: Optional[str] = None
    age: Optional[int] = None
    role: Optional[str] = "estudiante"

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, v: str) -> str:
        """Valida que el email tenga dominio @unal.edu.co"""
        if not v.lower().endswith("@unal.edu.co"):
            raise ValueError("Solo se permiten correos con dominio @unal.edu.co")
        return v.lower()

    # normalización de campos de texto para consistencia
    @field_validator("role", "gender", "major", mode="before")
    @classmethod
    def normalize_text_fields(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str):
            return v.strip().lower()
        return v


class UserOut(BaseModel):
    """Schema para mostrar la información de un usuario (sin la contraseña)"""

    id: int
    created_at: datetime
    name: str
    email: EmailStr
    role: str
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    major: Optional[str] = None
    age: Optional[int] = None
    rating: Optional[float] = None

    class Config:
        from_attributes = True  # Permite que Pydantic lea datos desde modelos ORM


class UserUpdate(BaseModel):
    """Schema para actualizar la información del usuario"""

    name: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    major: Optional[str] = None
    age: Optional[int] = None
    role: Optional[str] = None
    password: Optional[str] = None

    # normalización de campos de texto para consistencia
    @field_validator("gender", "major", "role", mode="before")
    @classmethod
    def normalize_text_fields(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str):
            return v.strip().lower()
        return v


class LoginRequest(BaseModel):
    """Schema para el login del usuario"""

    username: EmailStr
    password: str


class Token(BaseModel):
    """Schema para el token JWT"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema para los datos del token"""

    email: Optional[EmailStr] = None


class VehicleBase(BaseModel):
    """Schema base para datos de vehículo"""

    plate: str
    vehicle_type: str
    brand: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    year: Optional[int] = None
    notes: Optional[str] = None

    @field_validator("plate", mode="before")
    @classmethod
    def normalize_plate(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("La placa debe ser un texto válido")
        return v.strip().upper().replace(" ", "")

    @field_validator("vehicle_type", "brand", "model", "color", mode="before")
    @classmethod
    def normalize_vehicle_text_fields(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str):
            return v.strip().lower()
        return v


class VehicleCreate(VehicleBase):
    """Schema para crear un vehículo"""

    pass


class VehicleOut(VehicleBase):
    """Schema para mostrar la información del vehículo"""

    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
