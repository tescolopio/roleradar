## Multi-stage Dockerfile for RoleRadar (Flask + Gunicorn)
FROM python:3.11-slim AS base

# Environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app/src \
    ROLERADAR_WEB_MODE=1

WORKDIR /app

# System deps (minimal; cryptography has wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Install deps first for layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy source
COPY src /app/src
COPY roleradar.py scheduler.py /app/
COPY src/roleradar/dashboard/static /app/src/roleradar/dashboard/static
COPY src/roleradar/dashboard/templates /app/src/roleradar/dashboard/templates

# Create data dir for SQLite if using sqlite path override
RUN mkdir -p /data && chown -R root:root /data

# Expose service port
EXPOSE 8000

# Healthcheck hits Flask health endpoint (works when app running)
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8000/api/system/health || exit 1

# Default: run the web app via Gunicorn using the factory `create_app()`
# Bind on 0.0.0.0:8000 for containerized environments
# Use gevent workers for SSE/streaming support
# Increased timeout for AI processing operations
CMD ["gunicorn", "--worker-class", "gevent", "--workers", "3", "--timeout", "300", "--bind", "0.0.0.0:8000", "src.roleradar.dashboard.app:create_app()"]
