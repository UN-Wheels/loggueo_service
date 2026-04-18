from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.v1 import schemas
from app.core import security
from app.crud import vehicle as crud_vehicle
from app.db import models
from app.db.database import get_db

router = APIRouter()


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
