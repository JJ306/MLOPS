# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# System dependencies (optional: if you later need git, curl, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code and models
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start API
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]