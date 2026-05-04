# 🛒 Cart Microservice

Microservicio de **carrito de compras** desarrollado con **FastAPI** y **Redis**, diseñado como parte de una arquitectura de microservicios. Permite gestionar carritos de compras por usuario: agregar productos, consultar el carrito, modificar cantidades, y eliminar productos o vaciar el carrito completo.

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Tecnologías](#-tecnologías)
- [Arquitectura del Proyecto](#-arquitectura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Configuración y Ejecución](#-configuración-y-ejecución)
- [Ejecución de Tests](#-ejecución-de-tests)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Colección Postman](#-colección-postman)

---

## 📖 Descripción

Este microservicio gestiona el ciclo de vida del carrito de compras de un usuario. Cada carrito se almacena en **Redis** usando un Hash (`cart:{user_id}`) con un tiempo de expiración (TTL) de **24 horas**, lo que garantiza limpieza automática de carritos inactivos.

### Funcionalidades principales:
- ✅ **Agregar** productos al carrito
- ✅ **Consultar** el contenido del carrito
- ✅ **Modificar** la cantidad de un producto existente
- ✅ **Eliminar** un producto específico del carrito
- ✅ **Vaciar** el carrito completo
- ✅ **Health check** para monitoreo

---

## 🛠 Tecnologías

| Tecnología | Versión | Propósito |
|---|---|---|
| **Python** | 3.11 | Lenguaje principal |
| **FastAPI** | latest | Framework web asíncrono |
| **Redis** | 7 (Alpine) | Base de datos en memoria |
| **Uvicorn** | latest | Servidor ASGI |
| **Docker** | - | Contenerización |
| **Docker Compose** | 3.9 | Orquestación de servicios |
| **Pytest** | latest | Framework de testing |
| **HTTPX** | latest | Cliente HTTP para tests |

---

## 🏗 Arquitectura del Proyecto

```
cart-microservice/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Punto de entrada de la aplicación FastAPI
│   ├── redis_client.py          # Configuración y conexión a Redis
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── cart_controller.py   # Definición de rutas/endpoints
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── cart_repository.py   # Acceso directo a Redis (capa de datos)
│   └── services/
│       ├── __init__.py
│       └── cart_service.py      # Lógica de negocio y validaciones
├── tests/
│   ├── __init__.py
│   ├── test_cart_endpoints.py   # Tests del endpoint POST
│   ├── test_cart_repository.py  # Tests del repositorio
│   ├── test_get_cart.py         # Tests del endpoint GET
│   ├── test_put_item.py         # Tests del endpoint PUT
│   └── test_delete_item.py      # Tests del endpoint DELETE item
├── docs/
│   └── CartMicroservice.postman_collection.json
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

La aplicación sigue una **arquitectura en capas**:

1. **Controller** → Recibe las peticiones HTTP y delega al servicio.
2. **Service** → Aplica validaciones y lógica de negocio.
3. **Repository** → Interactúa directamente con Redis.

---

## 📌 Requisitos Previos

- [Docker](https://docs.docker.com/get-docker/) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) instalado
- (Opcional) [Python 3.11+](https://www.python.org/) si deseas ejecutar sin Docker

---

## 🚀 Configuración y Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/andres2225112/cart-microservice.git
cd cart-microservice
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` y configurar:

```env
REDIS_URL=redis://redis:6379
```

### 3. Levantar con Docker Compose

```bash
docker compose up --build
```

Esto levantará dos servicios:
- **cart_api** → API FastAPI en el puerto `8000`
- **cart_redis** → Redis en el puerto `6379`

### 4. Verificar que la API está corriendo

```bash
curl http://localhost:8000/health
```

Respuesta esperada:

```json
{ "status": "ok" }
```

### 5. Documentación interactiva (Swagger)

Acceder a: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Ejecución de Tests y Cobertura

Los tests se ejecutan con **pytest** y validan el correcto funcionamiento de los endpoints y la lógica del microservicio.

### Ejecutar tests básicos

```bash
pip install -r requirements.txt
pytest tests/ -v
```

---

### Reporte de cobertura en consola

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

Esto mostrará:

* Porcentaje de cobertura
* Líneas no cubiertas por tests

---

### Cobertura con umbral (80%) y reporte XML

```bash
pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=xml --cov-fail-under=80
```

* Falla si la cobertura es menor al **80%**
* Genera el archivo:

```text
coverage.xml
```

en la raíz del proyecto (usado en integración continua - CI)

---

### Tests incluidos

| Archivo                   | Descripción                          |
| ------------------------- | ------------------------------------ |
| `test_cart_endpoints.py`  | Tests para agregar items (POST)      |
| `test_get_cart.py`        | Tests para consultar carrito (GET)   |
| `test_put_item.py`        | Tests para actualizar cantidad (PUT) |
| `test_delete_item.py`     | Tests para eliminar item (DELETE)    |
| `test_cart_repository.py` | Tests unitarios del repositorio      |


---

## 📡 Endpoints de la API

Base URL: `http://localhost:8000`

### 1. Health Check

Verifica que el servicio está activo y la conexión a Redis.

| Campo           | Valor                                        |
| --------------- | -------------------------------------------- |
| **Método**      | `GET`                                        |
| **Ruta**        | `/health`                                    |
| **Descripción** | Verifica el estado del microservicio y Redis |

**Ejemplo de Response (200 OK):**

```json
{
  "status": "ok",
  "redis": "ok",
  "detail": null
}
```

**Ejemplo de Response (degradado):**

```json
{
  "status": "degraded",
  "redis": "error",
  "detail": "Connection refused"
}
```

### 2. Agregar producto al carrito

Agrega un producto al carrito del usuario. Si el producto ya existe, actualiza la cantidad.

| Campo | Valor |
|---|---|
| **Método** | `POST` |
| **Ruta** | `/api/cart/{userId}/items` |
| **Descripción** | Agrega un producto al carrito |
| **Content-Type** | `application/json` |

**Parámetros de ruta:**

| Parámetro | Tipo | Descripción |
|---|---|---|
| `userId` | `string` | Identificador del usuario |

**Body (JSON):**

| Campo | Tipo | Requerido | Descripción |
|---|---|---|---|
| `product_id` | `string` | ✅ | Identificador del producto |
| `quantity` | `integer` | ✅ | Cantidad (debe ser > 0) |

**Ejemplo de Request:**

```bash
POST /api/cart/user_123/items
Content-Type: application/json

{
  "product_id": "producto_101",
  "quantity": 2
}
```

**Ejemplo de Response** (`201 Created`):

```json
{
  "user_id": "user_123",
  "product_id": "producto_101",
  "quantity": 2
}
```

**Errores posibles:**

| Código | Descripción |
|---|---|
| `422` | Cantidad inválida (≤ 0) o `product_id` vacío |
| `500` | Error interno del servidor |

---

### 3. Consultar carrito

Obtiene todos los productos del carrito de un usuario con el total de items.

| Campo | Valor |
|---|---|
| **Método** | `GET` |
| **Ruta** | `/api/cart/{userId}` |
| **Descripción** | Retorna el contenido del carrito del usuario |

**Parámetros de ruta:**

| Parámetro | Tipo | Descripción |
|---|---|---|
| `userId` | `string` | Identificador del usuario |

**Ejemplo de Request:**

```bash
GET /api/cart/user_123
```

**Ejemplo de Response** (`200 OK`):

```json
{
  "user_id": "user_123",
  "items": {
    "producto_101": 2,
    "producto_205": 1
  },
  "total_items": 3
}
```

**Errores posibles:**

| Código | Descripción |
|---|---|
| `404` | Carrito no encontrado o vacío |
| `500` | Error interno del servidor |

---

### 4. Tiempo de vida del carrito (TTL)

Retorna el tiempo restante antes de que el carrito expire.

| Campo           | Valor                                 |
| --------------- | ------------------------------------- |
| **Método**      | `GET`                                 |
| **Ruta**        | `/api/cart/{userId}/ttl`              |
| **Descripción** | Obtiene el tiempo de vida del carrito |

**Ejemplo de Response (200 OK):**

```json
{
  "user_id": "user_123",
  "ttl_seconds": 82400,
  "ttl_hours": 22.89,
  "warning": null
}
```

**Sin expiración:**

```json
{
  "user_id": "user_123",
  "ttl_seconds": -1,
  "ttl_hours": null,
  "warning": "Cart has no expiration set"
}
```

**Errores posibles:**

| Código | Descripción                      |
| ------ | -------------------------------- |
| `404`  | Carrito no encontrado o expirado |


### 5. Modificar cantidad de un producto

Actualiza la cantidad de un producto existente en el carrito.

| Campo | Valor |
|---|---|
| **Método** | `PUT` |
| **Ruta** | `/api/cart/{userId}/items/{itemId}` |
| **Descripción** | Modifica la cantidad de un producto en el carrito |
| **Content-Type** | `application/json` |

**Parámetros de ruta:**

| Parámetro | Tipo | Descripción |
|---|---|---|
| `userId` | `string` | Identificador del usuario |
| `itemId` | `string` | Identificador del producto |

**Body (JSON):**

| Campo | Tipo | Requerido | Descripción |
|---|---|---|---|
| `quantity` | `integer` | ✅ | Nueva cantidad (debe ser > 0) |

**Ejemplo de Request:**

```bash
PUT /api/cart/user_123/items/producto_101
Content-Type: application/json

{
  "quantity": 5
}
```

**Ejemplo de Response** (`200 OK`):

```json
{
  "user_id": "user_123",
  "product_id": "producto_101",
  "quantity": 5
}
```

**Errores posibles:**

| Código | Descripción |
|---|---|
| `422` | Cantidad inválida (≤ 0) o `product_id` vacío |
| `500` | Error interno del servidor |

**Nuevo comportamiento (Sprint 3):**

| Código | Descripción                          |
| ------ | ------------------------------------ |
| `404`  | Producto no encontrado en el carrito |


---

### 6. Eliminar un producto del carrito

Elimina un producto específico del carrito del usuario.

| Campo | Valor |
|---|---|
| **Método** | `DELETE` |
| **Ruta** | `/api/cart/{userId}/items/{itemId}` |
| **Descripción** | Elimina un producto del carrito |

**Parámetros de ruta:**

| Parámetro | Tipo | Descripción |
|---|---|---|
| `userId` | `string` | Identificador del usuario |
| `itemId` | `string` | Identificador del producto a eliminar |

**Ejemplo de Request:**

```bash
DELETE /api/cart/user_123/items/producto_101
```

**Ejemplo de Response** (`200 OK`):

```json
{
  "user_id": "user_123",
  "product_id": "producto_101"
}
```

**Errores posibles:**

| Código | Descripción |
|---|---|
| `422` | `product_id` vacío |
| `500` | Error interno del servidor |

**Nuevo comportamiento (Sprint 3):**

| Código | Descripción                          |
| ------ | ------------------------------------ |
| `404`  | Producto no encontrado en el carrito |


---

### 7. Vaciar carrito completo

Elimina todos los productos del carrito del usuario.

| Campo | Valor |
|---|---|
| **Método** | `DELETE` |
| **Ruta** | `/api/cart/{userId}` |
| **Descripción** | Elimina el carrito completo del usuario |

**Parámetros de ruta:**

| Parámetro | Tipo | Descripción |
|---|---|---|
| `userId` | `string` | Identificador del usuario |

**Ejemplo de Request:**

```bash
DELETE /api/cart/user_123
```

**Ejemplo de Response** (`200 OK`):

```json
{
  "user_id": "user_123",
  "message": "Carrito eliminado"
}
```

**Errores posibles:**

| Código | Descripción |
|---|---|
| `500` | Error interno del servidor |

---



## 📦 Colección Postman

Se incluye una colección de Postman con todos los endpoints preconfigurados:

📁 `docs/CartMicroservice.postman_collection.json`

### Cómo importarla:

1. Abrir **Postman**
2. Click en **Import**
3. Seleccionar el archivo `docs/CartMicroservice.postman_collection.json`
4. La variable `{{base_url}}` ya está configurada como `http://localhost:8000`

---

## 👥 Equipo de Desarrollo — Sprint 2

| Integrante | Responsabilidad |
|---|---|
| Angerson Steven | Endpoint PUT (modificar cantidad) |
| Andrés Martínez | Tests para endpoint PUT |
| Luige Alejandro | Endpoint DELETE item |
| Alex Sandoval | Tests para endpoint DELETE item |
| Cristian Eduardo | Endpoint DELETE carrito (vaciar carrito) |
| Johan Sebastián | Tests para endpoint DELETE carrito |
| Arley Eduardo | Colección Postman |
| Luis Santiago Tarazona | Documentación README |