# Loggeo Base - Servicio de Gestión de Usuarios

Este microservicio es responsable de la autenticación, login y gestión de información de usuarios en el sistema. Proporciona endpoints para el inicio de sesión, obtención de datos de usuario y actualización de información de perfil.

## Descripción General

El servicio **loggeo_base** actúa como el punto de entrada principal para la autenticación y gestión de sesiones de usuarios. Permite a los cliente autenticarse, obtener información de su perfil y actualizar datos personales de forma segura.

## Tecnologías

- **Python**: Lenguaje de programación principal.
- **Pydantic**: Para la validación de datos y modelos.
- **FastAPI**: Framework web para construir APIs REST.
- **SQLAlchemy**: ORM para interactuar con la base de datos.
- **JWT**: Para la generación y validación de tokens de acceso.
- **OAuth2**: Protocolo de autorización utilizado para la seguridad de endpoints.
- **PostgreSQL**: Base de datos relacional utilizada para almacenar la información de los usuarios.
- **Prometheus**: Para monitoreo y métricas del servicio.

## Flujo de Funcionamiento

```
┌─────────────────────────────────────────────────────────────────┐
│                     Cliente/Aplicación                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   Solicitud     │
                    │   HTTP/REST     │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼────┐         ┌───▼────┐         ┌────▼─────┐
   │ POST     │         │ GET    │         │ PUT      │
   │ /login   │         │ /user/ │         │ /user/   │
   └────┬────┘         │{id}   │         │{id}     │
        │              └────┬───┘         └────┬────┘
        │                   │                   │
   ┌────▼──────────────────┴───────────────┬──▼─────────┐
   │         Capa de Validación/Autenticación           │
   │  - Validar credenciales                           │
   │  - Validar token JWT                              │
   │  - Validar datos de actualización                  │
   └────┬──────────────────┬───────────────┬───────────┘
        │                  │               │
   ┌────▼──────────┬──────▼────┐    ┌─────▼───────┐
   │ Autenticación │ Obtención  │    │ Actualizar  │
   │ de Usuario    │ de Datos   │    │ Datos       │
   │              │            │    │             │
   │ 1. Hash Pass  │ 1. Búsqueda│   │ 1. Validar  │
   │ 2. JWT Token  │   en DB    │   │    datos    │
   │ 3. Respuesta  │ 2. Response│   │ 2. Encriptar│
   │    (Token)    │            │   │    Pass     │
   │              │            │   │ 3. Guardar  │
   └────┬──────────┴──┬─────────┘   │    en DB    │
        │             │              └─────┬───────┘
        │             │                    │
        └──────┬──────┴────────────────────┘
               │
        ┌──────▼──────────┐
        │  Base de Datos  │
        │  (PostgreSQL)   │
        │                 │
        │  - users        │
        │  - sessions     │
        │  - logs         │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │  Respuesta JSON │
        │  - Status Code  │
        │  - Token/Data   │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │ Cliente/App     │
        │ Recibe Response │
        └─────────────────┘
```

## Endpoints

### 1. **POST /login**

- **Descripción**: Autentica un usuario y genera un token JWT.
- **Parámetros**:
    - `email`: Email del usuario (string, requerido)
    - `password`: Contraseña del usuario (string, requerido)
- **Respuesta**:
    ```json
    {
        "access_token": "eyJhbGciOiJIUzI1N...",
        "token_type": "bearer",
        "user_id": 1,
        "email": "usuario@example.com"
    }
    ```

### 2. **GET /user/{id}**

- **Descripción**: Obtiene la información del usuario autenticado.
- **Autenticación**: Requiere token JWT válido.
- **Parámetros**:
    - `id`: ID del usuario (entero, requerido)
- **Respuesta**:
    ```json
    {
        "id": 1,
        "email": "usuario@example.com",
        "nombre": "Juan",
        "apellido": "Pérez",
        "teléfono": "+57 3001234567",
        "fecha_creacion": "2024-01-15T10:30:00Z"
    }
    ```

### 3. **PUT /user/{id}**

- **Descripción**: Actualiza la información del usuario (perfil, contraseña, etc.).
- **Autenticación**: Requiere token JWT válido.
- **Parámetros**:
    - `id`: ID del usuario (entero, requerido)
    - `nombre`: Nombre actualizado (string, opcional)
    - `apellido`: Apellido actualizado (string, opcional)
    - `teléfono`: Número de teléfono (string, opcional)
    - `password`: Nueva contraseña (string, opcional)
- **Respuesta**:
    ```json
    {
        "mensaje": "Usuario actualizado exitosamente",
        "usuario": {
            "id": 1,
            "email": "usuario@example.com",
            "nombre": "Juan",
            "apellido": "Pérez"
        }
    }
    ```

### 4. **POST /logout**

- **Descripción**: Invalida el token JWT del usuario.
- **Autenticación**: Requiere token JWT válido.
- **Respuesta**:
    ```json
    {
        "mensaje": "Sesión cerrada exitosamente"
    }
    ```

## Configuración

### 1. Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Base de datos
DATABASE_URL=postgresql://user:password@localhost:5432/loggeo_base_db

# Seguridad
SECRET_KEY=tu_clave_secreta_muy_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Servidor
DEBUG=True
ENVIRONMENT=development

# Prometheus
PROMETHEUS_PORT=8001
```

### 2. Crear Entorno Virtual

```bash
# En Windows
py -m venv venv
venv\Scripts\activate

# En Linux o macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar Migraciones de Base de Datos (si aplica)

```bash
# Crear tablas en la base de datos
python -c "from app.db.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### 5. Iniciar el Servidor

```bash
# Modo desarrollo con recarga automática
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Modo producción
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

El servicio estará disponible en: `http://localhost:8000`

## Docker

Se incluyeron archivos para ejecutar el servicio completo con contenedores:

- `Dockerfile`: imagen de la API FastAPI
- `docker-compose.yml`: API + PostgreSQL
- `.dockerignore`: exclusiones para acelerar build

### Ejecutar con Docker Compose

Primero, cree su archivo de entorno local:

```bash
cp .env.example .env
```

```bash
docker compose up --build
```

La API quedará disponible en `http://localhost:8000` y la base de datos en `localhost:5432`.

Para detener y eliminar contenedores:

```bash
docker compose down
```

Para detener y eliminar también el volumen de PostgreSQL:

```bash
docker compose down -v
```

## Probar los Endpoints

### Opción 1: Swagger UI (Recomendado)

Acceda a la documentación interactiva en: `http://localhost:8000/docs`

### Opción 2: ReDoc

Acceda a la documentación alternativa en: `http://localhost:8000/redoc`

### Opción 3: Postman o cURL

**Ejemplo - Login:**

```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "password": "password123"
  }'
```

**Ejemplo - Obtener Usuario:**

```bash
curl -X GET "http://localhost:8000/user/1" \
  -H "Authorization: Bearer <access_token>"
```

**Ejemplo - Actualizar Usuario:**

```bash
curl -X PUT "http://localhost:8000/user/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "nombre": "Carlos",
    "teléfono": "+57 3009876543"
  }'
```

## Monitoreo

El servicio incluye métricas de Prometheus disponibles en: `http://localhost:8001/metrics`

### Métricas Disponibles:

- `http_requests_total`: Total de solicitudes HTTP
- `http_request_duration_seconds`: Duración de las solicitudes
- `login_attempts_total`: Total de intentos de login
- `auth_errors_total`: Total de errores de autenticación

## Estructura de Carpetas

```
loggeo_base/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada de la aplicación
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py     # Endpoints de login/logout
│   │   │   │   └── users.py    # Endpoints de usuarios
│   │   │   └── schemas.py      # Esquemas Pydantic
│   ├── core/
│   │   ├── config.py           # Configuración
│   │   └── security.py         # Funciones de seguridad
│   ├── db/
│   │   ├── database.py         # Conexión a BD
│   │   └── models.py           # Modelos SQLAlchemy
│   ├── crud/
│   │   ├── user.py             # Operaciones CRUD de usuarios
│   │   └── session.py          # Operaciones CRUD de sesiones
│   └── metrics/
│       └── prometheus.py       # Métricas de Prometheus
├── tests/                       # Tests unitarios
├── .env                         # Variables de entorno
├── requirements.txt             # Dependencias Python
└── README.md                    # Este archivo
```

## Dependencias Principales

Ver `requirements.txt` para la lista completa. Principales:

- `fastapi>=0.104.0`
- `sqlalchemy>=2.0.0`
- `pydantic>=2.0.0`
- `python-jose[cryptography]>=3.3.0`
- `passlib[bcrypt]>=1.7.4`
- `psycopg2-binary>=2.9.0`
- `prometheus-client>=0.18.0`

## Contribuiendo

1. Crear una rama para la nueva funcionalidad: `git checkout -b feature/nueva-funcionalidad`
2. Hacer commit de los cambios: `git commit -am 'Agregar nueva funcionalidad'`
3. Hacer push a la rama: `git push origin feature/nueva-funcionalidad`
4. Abrir un Pull Request

## Licencia

Este proyecto está bajo licencia MIT. Ver `LICENSE` para más detalles.

## Contacto

Para preguntas o soporte, contactar al equipo de desarrollo.
