# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

# Expose the port that FastAPI will run on
EXPOSE 8800

# Command to run the FastAPI app with Uvicorn and enable auto-reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8800", "--reload"]
