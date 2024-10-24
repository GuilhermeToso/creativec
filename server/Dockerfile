# Use an official Python runtime as a parent image (Python 3.11)
FROM python:3.11-slim

# Set the working directory to /app/server
WORKDIR /app/server

# Copy only the relevant directories from the root project directory
COPY src /app/server/src
COPY assets /app/server/assets
COPY requirements.txt /app/server/requirements.txt

# Install dependencies directly in the container
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run FastAPI (using uvicorn)
CMD ["uvicorn", "server.src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]