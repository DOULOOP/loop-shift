FROM python:3.9-slim

# Install system dependencies required for build and hardware access
# libgpiod-dev and python3-dev are often needed for GPIO access on RPi
# i2c-tools is helpful for debugging
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    i2c-tools \
    libgpiod2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port for FastAPI
EXPOSE 8000

# We'll use an environment variable to decide whether to run the API or the CLI
# Default to API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

