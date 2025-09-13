# Use official Python runtime as base
FROM python:3.11-slim

# Set work directory inside container
WORKDIR /app

# Install system dependencies (needed for psycopg2/mysqlclient, etc.)
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first to leverage Docker layer caching
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend project into the container
COPY . .

# Expose the port Django/Gunicorn will listen on
EXPOSE 8000

# Start Gunicorn when the container starts
CMD ["gunicorn", "tinyurl.wsgi:application", "--bind", "0.0.0.0:8000"]
