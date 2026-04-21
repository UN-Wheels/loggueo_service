from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.v1 import schemas
from app.core import security
from app.crud import vehicle as crud_vehicle
from app.db import models
from app.db.database import get_db

router = APIRouter()


@router.get("/", response_model=list[schemas.VehicleOut])
def get_my_vehicles(
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
):
    """Obtiene todos los vehículos del usuario autenticado."""
    return crud_vehicle.get_user_vehicles(db=db, owner_id=current_user.id)


@router.get("/public/{vehicle_id}", response_model=schemas.VehiclePublic)
def get_vehicle_public(
    vehicle_id: int,
    _: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
):
    """Retorna información pública de un vehículo por ID (sin verificar ownership).
    Usado por el gateway para enriquecer respuestas de rutas."""
    vehicle = crud_vehicle.get_vehicle_by_id(db=db, vehicle_id=vehicle_id)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado",
        )
    return vehicle


@router.get("/{vehicle_id}", response_model=schemas.VehicleOut)
def get_my_vehicle(
    vehicle_id: int,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
):
    """Obtiene un vehículo específico si pertenece al usuario autenticado."""
    vehicle = crud_vehicle.get_vehicle_by_id_and_owner(
        db=db,
        vehicle_id=vehicle_id,
        owner_id=current_user.id,
    )

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado para este usuario",
        )

    return vehicle


@router.post("/", response_model=schemas.VehicleOut, status_code=201)
def create_my_vehicle(
    vehicle_in: schemas.VehicleCreate,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
):
    """Crea un vehículo para el usuario autenticado."""
    created_vehicle = crud_vehicle.create_vehicle(
        db=db,
        owner_id=current_user.id,
        vehicle_in=vehicle_in,
    )

    if not created_vehicle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo crear el vehículo. Verifique que la placa no exista.",
        )

    return created_vehicle


@router.delete("/{vehicle_id}", status_code=204)
def delete_my_vehicle(
    vehicle_id: int,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
):
    """Elimina un vehículo solo si pertenece al usuario autenticado."""
    deleted = crud_vehicle.delete_vehicle(
        db=db,
        vehicle_id=vehicle_id,
        owner_id=current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado para este usuario",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
