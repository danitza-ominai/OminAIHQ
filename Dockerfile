# OminAI HQ - Contenedor de Despliegue Cloud Run (PZ-014A)
FROM python:3.11-slim

# Evitar escritura de bytecode y habilitar buffer sin retraso
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Instalar el cierre completo resuelto para Python 3.11/Linux.
COPY pyproject.toml .
COPY deploy/requirements.lock ./requirements.lock
RUN python -m pip install --no-cache-dir --require-hashes -r requirements.lock

# Copiar codigo fuente del producto, contratos y assets web
COPY app/ app/
COPY contracts/ contracts/
COPY evaluation/ evaluation/
COPY web/ web/
COPY README.md .

# Crear usuario sin privilegios root
RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

CMD ["python", "-B", "-m", "app.cloud_http_api"]
