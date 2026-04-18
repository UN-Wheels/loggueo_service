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
   ┌────▼────────┐    ┌───▼─────┐        ┌────▼──────┐
   │ POST         │    │ GET     │        │ POST/PUT  │
   │ /register    │    │ /me     │        │ /me       │
   │ /login       │    │         │        │           │
   └────┬────────┘    └────┬────┘        └────┬──────┘
        │                  │                   │
   ┌────▼──────────────────┴───────────────┬──▼─────────┐
   │      Capa de Validación/Autenticación             │
   │  - Validar credenciales                          │
   │  - Validar token JWT                             │
   │  - Validar datos (email @unal.edu.co)            │
   └────┬──────────────────┬───────────────┬──────────┘
        │                  │               │
   ┌────▼──────────┬──────▼────┐    ┌─────▼──────┐
   │ Autenticación │ Obtención  │    │ Actualizar │
   │ de Usuario    │ de Datos   │    │ Datos      │
   │              │            │    │            │
   │ 1. Hash Pass  │ 1. Búsqueda│   │ 1. Validar │
   │ 2. JWT Token  │   en DB    │   │    datos   │
   │ 3. Respuesta  │ 2. Response│   │ 2. Guardar │
   │    (Token)    │            │   │    en DB   │
   │              │            │   │            │
   └────┬──────────┴──┬─────────┘   └─────┬──────┘
        │             │                   │
        └──────┬──────┴───────────────────┘
               │
        ┌──────▼──────────┐
        │  Base de Datos  │
        │  (PostgreSQL)   │
        │                 │
        │  - users        │
        │  - user_logs    │
        │  - vehicles     │
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

### 1. **POST /api/v1/auth/register**

- **Descripción**: Registra un nuevo usuario.
- **Validaciones**: El email debe tener dominio @unal.edu.co
- **Body** (JSON):
    ```json
    {
        "name": "Juan Pérez",
        "email": "juan.perez@unal.edu.co",
        "password": "password123",
        "phone_number": "+57 3001234567",
        "gender": "masculino",
        "major": "ingeniería",
        "age": 22,
        "role": "estudiante"
    }
    ```
- **Respuesta** (201 Created):
    ```json
    {
        "id": 1,
        "created_at": "2024-01-15T10:30:00Z",
        "name": "Juan Pérez",
        "email": "juan.perez@unal.edu.co",
        "role": "estudiante",
        "phone_number": "+57 3001234567",
        "gender": "masculino",
        "major": "ingeniería",
        "age": 22,
        "rating": 0.0
    }
    ```

### 2. **POST /api/v1/auth/login**

- **Descripción**: Autentica un usuario y genera un token JWT.
- **Body** (JSON):
    ```json
    {
        "username": "juan.perez@unal.edu.co",
        "password": "password123"
    }
    ```
- **Respuesta**:
    ```json
    {
        "access_token": "eyJhbGciOiJIUzI1N...",
        "token_type": "bearer"
    }
    ```

### 3. **GET /api/v1/auth/me**

- **Descripción**: Obtiene la información del usuario autenticado (basado en el token JWT).
- **Autenticación**: Requiere token JWT válido.
- **Respuesta**:
    ```json
    {
        "id": 1,
        "created_at": "2024-01-15T10:30:00Z",
        "name": "Juan Pérez",
        "email": "usuario@unal.edu.co",
        "role": "estudiante",
        "phone_number": "+57 3001234567",
        "gender": "masculino",
        "major": "ingeniería",
        "age": 22,
        "rating": 4.5
    }
    ```

### 4. **PUT /api/v1/auth/me**

- **Descripción**: Actualiza la información del usuario autenticado.
- **Autenticación**: Requiere token JWT válido.
- **Parámetros**:
    - `name`: Nombre actualizado (string, opcional)
    - `phone_number`: Número de teléfono (string, opcional)
    - `gender`: Género (string, opcional)
    - `major`: Carrera o especialidad (string, opcional)
    - `age`: Edad (entero, opcional)
    - `password`: Nueva contraseña (string, opcional)
- **Respuesta**:
    ```json
    {
        "id": 1,
        "created_at": "2024-01-15T10:30:00Z",
        "name": "Juan Pérez",
        "email": "usuario@unal.edu.co",
        "role": "estudiante",
        "phone_number": "+57 3001234567",
        "gender": "masculino",
        "major": "ingeniería",
        "age": 22,
        "rating": 4.5
    }
    ```

## Gestión de Vehículos

El servicio incluye un sistema completo de gestión de vehículos. Cada usuario puede tener múltiples vehículos, y la relación es de uno-a-muchos (1 usuario : N vehículos). Un vehículo pertenece a un único usuario.

### Campos del Vehículo

| Campo | Tipo | Requerido | Descripción |
| --- | --- | --- | --- |
| `id` | Entero | Sí (generado) | Identificador único del vehículo |
| `user_id` | Entero | Sí | ID del usuario propietario |
| `created_at` | DateTime | Sí (generado) | Fecha de creación |
| `plate` | String | Sí | Placa del vehículo (única, normalizada a mayúsculas sin espacios) |
| `vehicle_type` | String | Sí | Tipo de vehículo (ej: carro, moto, bicicleta) |
| `brand` | String | No | Marca del vehículo (ej: Mazda, Toyota) |
| `model` | String | No | Modelo del vehículo (ej: Civic, 3 Series) |
| `color` | String | No | Color del vehículo |
| `year` | Entero | No | Año de fabricación |
| `notes` | String | No | Notas adicionales sobre el vehículo |

### Endpoints de Vehículos

### 5. **GET /api/v1/vehicles/**

- **Descripción**: Obtiene todos los vehículos del usuario autenticado.
- **Autenticación**: Requiere token JWT válido.
- **Respuesta** (array de vehículos):
    ```json
    [
        {
            "id": 1,
            "user_id": 1,
            "created_at": "2024-01-20T14:30:00Z",
            "plate": "ABC123",
            "vehicle_type": "carro",
            "brand": "mazda",
            "model": "3",
            "color": "rojo",
            "year": 2022,
            "notes": "Uso diario"
        },
        {
            "id": 2,
            "user_id": 1,
            "created_at": "2024-01-21T09:15:00Z",
            "plate": "XYZ789",
            "vehicle_type": "moto",
            "brand": "yamaha",
            "model": "ybr 125",
            "color": "negro",
            "year": 2021,
            "notes": "Fines de semana"
        }
    ]
    ```

### 6. **GET /api/v1/vehicles/{vehicle_id}**

- **Descripción**: Obtiene los detalles de un vehículo específico si pertenece al usuario autenticado.
- **Autenticación**: Requiere token JWT válido.
- **Parámetros**:
    - `vehicle_id`: ID del vehículo (entero, requerido en URL)
- **Respuesta**:
    ```json
    {
        "id": 1,
        "user_id": 1,
        "created_at": "2024-01-20T14:30:00Z",
        "plate": "ABC123",
        "vehicle_type": "carro",
        "brand": "mazda",
        "model": "3",
        "color": "rojo",
        "year": 2022,
        "notes": "Uso diario"
    }
    ```
- **Errores**:
    - `404`: Vehículo no encontrado para este usuario

### 7. **POST /api/v1/vehicles/**

- **Descripción**: Crea un nuevo vehículo para el usuario autenticado.
- **Autenticación**: Requiere token JWT válido.
- **Body** (JSON):
    ```json
    {
        "plate": "ABC 123",
        "vehicle_type": "carro",
        "brand": "mazda",
        "model": "3",
        "color": "rojo",
        "year": 2022,
        "notes": "Uso diario"
    }
    ```
- **Validaciones**:
    - `plate`: Requerido. Se normaliza automáticamente (mayúsculas, sin espacios).
    - `vehicle_type`: Requerido. Se convierte a minúsculas.
    - Otros campos: Opcionales. Texto se convierte a minúsculas.
    - La placa debe ser única en el sistema.
- **Respuesta** (201 Created):
    ```json
    {
        "id": 3,
        "user_id": 1,
        "created_at": "2024-01-22T10:45:00Z",
        "plate": "ABC123",
        "vehicle_type": "carro",
        "brand": "mazda",
        "model": "3",
        "color": "rojo",
        "year": 2022,
        "notes": "uso diario"
    }
    ```
- **Errores**:
    - `400`: No se pudo crear el vehículo (ej: placa duplicada)

### 8. **DELETE /api/v1/vehicles/{vehicle_id}**

- **Descripción**: Elimina un vehículo del usuario autenticado.
- **Autenticación**: Requiere token JWT válido.
- **Parámetros**:
    - `vehicle_id`: ID del vehículo (entero, requerido en URL)
- **Respuesta** (204 No Content):
    ```
    (Sin cuerpo)
    ```
- **Errores**:
    - `404`: Vehículo no encontrado para este usuario

## Esquema de Base de Datos

### Tablas Principales

#### **users**

Almacena la información de los usuarios del sistema.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    name VARCHAR NOT NULL,
    role VARCHAR NOT NULL DEFAULT 'estudiante',
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    phone_number VARCHAR,
    gender VARCHAR,
    major VARCHAR,
    age INTEGER,
    rating FLOAT DEFAULT 0.0
);
```

#### **vehicles**

Almacena la información de los vehículos de cada usuario. Relación uno-a-muchos con la tabla `users`.

```sql
CREATE TABLE vehicles (
    id INTEGER PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plate VARCHAR UNIQUE NOT NULL,
    vehicle_type VARCHAR NOT NULL,
    brand VARCHAR,
    model VARCHAR,
    color VARCHAR,
    year INTEGER,
    notes VARCHAR
);
```

#### **user_logs**

Registra los intentos de login de los usuarios.

```sql
CREATE TABLE user_logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    email VARCHAR NOT NULL,
    login_time TIMESTAMP NOT NULL,
    token VARCHAR NOT NULL
);
```

### Relaciones

- **users ↔ vehicles**: Un usuario puede tener muchos vehículos, pero cada vehículo pertenece a un único usuario.
    - Clave foránea: `vehicles.user_id` → `users.id`
    - Cascada: Si se elimina un usuario, se eliminan todos sus vehículos automáticamente.

- **users ↔ user_logs**: Un usuario puede tener muchos logs de login.
    - Clave foránea: `user_logs.user_id` → `users.id`

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

**Ejemplo - Register:**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan.perez@unal.edu.co",
    "password": "password123",
    "phone_number": "+57 3001234567",
    "gender": "masculino",
    "major": "ingeniería",
    "age": 22
  }'
```

**Ejemplo - Login:**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan.perez@unal.edu.co",
    "password": "password123"
  }'
```

**Ejemplo - Obtener datos del usuario autenticado:**

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer <access_token>"
```

**Ejemplo - Actualizar usuario:**

```bash
curl -X PUT "http://localhost:8000/api/v1/auth/me" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "phone_number": "+57 3009876543",
    "age": 23
  }'
```

**Ejemplo - Obtener todos los vehículos:**

```bash
curl -X GET "http://localhost:8000/api/v1/vehicles/" \
  -H "Authorization: Bearer <access_token>"
```

**Ejemplo - Obtener un vehículo específico:**

```bash
curl -X GET "http://localhost:8000/api/v1/vehicles/1" \
  -H "Authorization: Bearer <access_token>"
```

**Ejemplo - Crear vehículo:**

```bash
curl -X POST "http://localhost:8000/api/v1/vehicles/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "plate": "ABC 123",
    "vehicle_type": "carro",
    "brand": "mazda",
    "model": "3",
    "color": "rojo",
    "year": 2022,
    "notes": "Uso diario"
  }'
```

**Ejemplo - Eliminar vehículo:**

```bash
curl -X DELETE "http://localhost:8000/api/v1/vehicles/1" \
  -H "Authorization: Bearer <access_token>"
```

## Estructura de Carpetas

```
loggeo_base/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada de la aplicación
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py       # Endpoints de autenticación
│   │   │   │   └── vehicles.py   # Endpoints de gestión de vehículos
│   │   │   └── schemas.py        # Esquemas Pydantic
│   ├── core/
│   │   ├── config.py             # Configuración
│   │   └── security.py           # Funciones de seguridad
│   ├── db/
│   │   ├── database.py           # Conexión a BD
│   │   └── models.py             # Modelos SQLAlchemy (User, UserLog, Vehicle)
│   └── crud/
│       ├── user.py               # Operaciones CRUD de usuarios
│       └── vehicle.py            # Operaciones CRUD de vehículos
├── tests/                         # Tests unitarios
├── .env                           # Variables de entorno
├── requirements.txt               # Dependencias Python
├── Dockerfile                     # Configuración Docker
├── docker-compose.yml             # Orquestación Docker
└── README.md                      # Este archivo
```

## Dependencias Principales

Ver `requirements.txt` para la lista completa. Principales:

- `fastapi>=0.104.0`
- `sqlalchemy>=2.0.0`
- `pydantic>=2.0.0`
- `python-jose[cryptography]>=3.3.0`
- `passlib[bcrypt]>=1.7.4`
- `psycopg2-binary>=2.9.0`

## Contribuiendo

1. Crear una rama para la nueva funcionalidad: `git checkout -b feature/nueva-funcionalidad`
2. Hacer commit de los cambios: `git commit -am 'Agregar nueva funcionalidad'`
3. Hacer push a la rama: `git push origin feature/nueva-funcionalidad`
4. Abrir un Pull Request

## Licencia

Este proyecto está bajo licencia MIT. Ver `LICENSE` para más detalles.

## Contacto

Para preguntas o soporte, contactar al equipo de desarrollo.
