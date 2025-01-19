# Use the official Python image with Ubuntu
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the script into the container
COPY run.py /app/run.py

# Expose the port for Netcat connection
EXPOSE 12345

# Run the script when the container starts
CMD ["python3", "/app/run.py"]
