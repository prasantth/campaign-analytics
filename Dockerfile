# Use an official Python image as the base image
FROM python:3.12-slim

# Install dependencies for PostgreSQL and Python
RUN apt-get update && apt-get install -y \
    postgresql postgresql-contrib libpq-dev gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables (these will be overwritten by .env file)
ENV DB_NAME=nike_campaign_data \
    DB_USER=postgres \
    DB_PASSWORD=postgres \
    DB_HOST=localhost \
    DB_PORT=5432

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code to the container
COPY . .

# Build the MkDocs documentation
RUN mkdocs build -f my-docs/mkdocs.yml

# Initialize PostgreSQL, update password, and create database
USER postgres
RUN service postgresql start && \
    psql --command "ALTER USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';" && \
    psql --command "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"

# Switch back to root to run Python script and FastAPI service
USER root

# Run the script to insert data into the database
RUN service postgresql start && \
    python3 src/utils/insert_data_to_postgres.py

# Expose the FastAPI port (default FastAPI runs on port 8000)
EXPOSE 8800

# Expose the MkDocs server port
EXPOSE 5500

# Start PostgreSQL service, FastAPI app, and MkDocs server
CMD sh -c "service postgresql start && uvicorn main:app --host 0.0.0.0 --port 8800 & mkdocs serve -f my-docs/mkdocs.yml --dev-addr=0.0.0.0:5500"