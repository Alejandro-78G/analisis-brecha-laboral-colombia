FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos del proyecto
COPY pyproject.toml .env.example README.md ./
COPY src/ ./src/
COPY dbt_project/ ./dbt_project/
COPY tests/ ./tests/

# Instalar dependencias de Python
RUN pip install --no-cache-dir -e .

EXPOSE 8501

CMD ["streamlit", "run", "src/dashboard/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
