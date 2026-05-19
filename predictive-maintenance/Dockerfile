# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies if needed (kept minimal for now)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list first (better for Docker caching)
COPY requirements_docker.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements_docker.txt

# Copy the rest of the project into the image
# (src/, models/, data config, etc.)
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Default command: start FastAPI app
# NOTE: this matches your current layout: src/api/app.py and 'app' object inside
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]