from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import models
from app.api.v1 import schemas


def create_vehicle(db: Session, owner_id: int, vehicle_in: schemas.VehicleCreate):
    """Crea un nuevo vehículo asociado a un usuario."""
    try:
        db_vehicle = models.Vehicle(
            user_id=owner_id,
            plate=vehicle_in.plate,
            vehicle_type=vehicle_in.vehicle_type,
            brand=vehicle_in.brand,
            model=vehicle_in.model,
            color=vehicle_in.color,
            year=vehicle_in.year,
            notes=vehicle_in.notes,
        )
        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)
        return db_vehicle
    except IntegrityError:
        db.rollback()
        return None
    except Exception as e:
        db.rollback()
        print(f"Error creating vehicle: {e}")
        return None


def get_user_vehicles(db: Session, owner_id: int):
    """Obtiene todos los vehículos de un usuario."""
    return db.query(models.Vehicle).filter(models.Vehicle.user_id == owner_id).all()


def get_vehicle_by_id_and_owner(db: Session, vehicle_id: int, owner_id: int):
    """Obtiene un vehículo por su id verificando que pertenezca al usuario."""
    return (
        db.query(models.Vehicle)
        .filter(models.Vehicle.id == vehicle_id, models.Vehicle.user_id == owner_id)
        .first()
    )


def delete_vehicle(db: Session, vehicle_id: int, owner_id: int) -> bool:
    """Elimina un vehículo solo si pertenece al usuario autenticado."""
    vehicle = get_vehicle_by_id_and_owner(db, vehicle_id=vehicle_id, owner_id=owner_id)
    if not vehicle:
        return False

    try:
        db.delete(vehicle)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error deleting vehicle: {e}")
        return False
