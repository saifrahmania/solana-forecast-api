# ===============================================================
# 1. Base image
# ===============================================================
FROM python:3.11-slim

# ===============================================================
# 2. Environment settings
# ===============================================================
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# ===============================================================
# 3. System dependencies (OpenMP, curl, build tools)
# ===============================================================
RUN apt-get update -y && apt-get install -y --no-install-recommends \
      build-essential \
      libgomp1 \
      libstdc++6 \
      curl \
  && rm -rf /var/lib/apt/lists/*

# ===============================================================
# 4. Set working directory
# ===============================================================
WORKDIR /app

# ===============================================================
# 5. Install Python dependencies
# ===============================================================
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ===============================================================
# 6. Copy application files only (clean image)
# ===============================================================
COPY app ./app
COPY artifacts ./artifacts
COPY README.md ./README.md

# ===============================================================
# 7. Create non-root user for security
# ===============================================================
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# ===============================================================
# 8. Expose API port
# ===============================================================
EXPOSE 8000

# ===============================================================
# 9. Healthcheck (optional but recommended)
# ===============================================================
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1

# ===============================================================
# 10. Start FastAPI with Uvicorn
# ===============================================================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
