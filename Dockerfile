# Usar imagen oficial de Python optimizada para Render
FROM python:3.11-slim

# Instalar dependencias del sistema mínimas
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio para bases de datos
RUN mkdir -p database

# Exponer puerto dinámico (Render asigna automáticamente)
EXPOSE $PORT

# Comando para ejecutar la aplicación
CMD ["sh", "-c", "python scripts/init_render.py && python app.py"]