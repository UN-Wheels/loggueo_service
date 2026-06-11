# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.database import get_db, get_db_read
from app.crud import user as crud_user
from app.api.v1 import schemas
from app.core import security
from app.core.config import settings
from app.db import models

router = APIRouter()


@router.post("/register", response_model=schemas.UserOut, status_code=201)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registrar un nuevo usuario.
    
    Valida que:
    - El correo tenga dominio @unal.edu.co
    - El correo no esté ya registrado
    - Los datos cumplan con los esquemas requeridos
    """
    # Verificar que el email no esté ya registrado
    db_user = crud_user.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )
    
    # Crear el usuario en la base de datos
    new_user = crud_user.create_user(db=db, user=user_in)
    
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el usuario"
        )
    
    return new_user


@router.post("/login", response_model=schemas.Token)
def login_for_access_token(
    login_data: schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    """Permite al usuario autenticarse y devuelve un token JWT."""
    user = crud_user.authenticate_user(db, email=login_data.username, password=login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires,
    )
    
    # Registrar el login en la tabla de logs con el token
    crud_user.create_login_log(
        db=db,
        user_id=user.id,
        email=user.email,
        token=access_token
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserOut)
def read_current_user(
    current_user: models.User = Depends(security.get_current_user)
):
    """Retorna la información del usuario autenticado según el token."""
    return current_user


@router.get("/users/{user_email}", response_model=schemas.UserPublic)
def get_user_by_email(
    user_email: str,
    _: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db_read),
):
    """Retorna la información pública de un usuario por su email (usado como ID)."""
    user = crud_user.get_user_by_email(db, email=user_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return user


@router.put("/me", response_model=schemas.UserOut)
def update_current_user(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    """Actualiza la información del usuario autenticado.
    
    Solo el usuario autenticado puede actualizar su propia información.
    Los campos no enviados no se modificarán.
    """
    updated_user = crud_user.update_user(db=db, user=current_user, user_update=user_update)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el usuario"
        )
    
    return updated_user
