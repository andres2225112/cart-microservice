# Cart Microservice

Microservicio de carrito de compras desarrollado con FastAPI + Redis.


## Cómo correr el proyecto localmente

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/[usuario]/cart-microservice.git
   cd cart-microservice
   ```

2. Copiar el archivo de variables de entorno:

   ```bash
   cp .env.example .env
   ```

   Editar `.env` y poner los valores correctos (para local usar `REDIS_URL=redis://redis:6379`).

3. Levantar con Docker Compose:

   ```bash
   docker compose up --build
   ```

4. La API estará disponible en: <http://localhost:8000>

5. Documentación automática (Swagger): <http://localhost:8000/docs>