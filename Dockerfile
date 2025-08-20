# Use Python 3.12.3 slim image as base
FROM python:3.12.3-slim

WORKDIR /app

# Install system dependencies including build tools
RUN apt-get update && apt-get install -y \
    vim \
    curl \
    gcc \
    g++ \
    make \
    libffi-dev \
    flex \
    bison \
    libtool \
    pkg-config \
    git \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Copy entrypoint script
COPY entrypoint.sh /app/

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Command to run the application
CMD ["python", "manage.py", "runserver"]