# app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api.v1.endpoints import auth, vehicles
from app.db import models, database

# Crear las tablas en la base de datos si no existen
try:
    models.Base.metadata.create_all(bind=database.engine_primary)
    print("✓ Tablas de la base de datos creadas (si no existían).")
except Exception as e:
    print(f"✗ Error al crear las tablas de la base de datos: {e}")

# Crear instancia de FastAPI
app = FastAPI(
    title="Loggeo Base - Servicio de Autenticación",
    description="Microservicio de autenticación y gestión de usuarios para UIFCE",
    version="0.1.0",
)

# Configurar CORS
_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173")
_allowed_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers de autenticación
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticación"])
app.include_router(vehicles.router, prefix="/api/v1/vehicles", tags=["Vehículos"])


# Endpoint de salud
@app.get("/", tags=["Health"])
def read_root():
    """Endpoint de verificación de estado del servicio."""
    return {"status": "ok", "service": "loggeo-base-service"}


# Personalizar esquema OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Loggeo Base - Servicio de Autenticación",
        version="0.1.0",
        description="Microservicio de autenticación y gestión de usuarios",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
