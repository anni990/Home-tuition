# Use official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    unixodbc \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Add Microsoft ODBC Driver for SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# Install MySQL client
RUN apt-get update && apt-get install -y default-mysql-client default-libmysqlclient-dev build-essential pkg-config

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create uploads directory if it doesn't exist
RUN mkdir -p app/static/uploads

# Expose port
EXPOSE 5000

# Command to run the application
CMD ["python", "run.py"] 