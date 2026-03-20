# Imagen base oficial de Python slim (más liviana)
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar dependencias primero (aprovecha caché de Docker)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Puerto que expone la aplicación
EXPOSE 8000

# Comando para correr el servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
