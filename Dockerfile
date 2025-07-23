# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y \
  build-essential \
  libpq-dev \
  gcc \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run the app
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000 --timeout 0"]
