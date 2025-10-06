# Imagen base con Python
FROM python:3.12-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos requirements y los instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto
COPY . .

# Comando por defecto
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]

