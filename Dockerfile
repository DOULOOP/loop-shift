FROM python:3.9

# Install system dependencies required for hardware access
# i2c-tools is helpful for debugging, libgpiod2 for GPIO
RUN apt-get update && apt-get install -y \
    libgpiod-dev \
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



