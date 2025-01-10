# Use slim version of Python 3.10 for smaller image size
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only the necessary files
COPY run.py /app/
COPY requirements.txt /app/

# Install dependencies (if any)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 12345

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Run as non-root user for better security
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Command to run the application
CMD ["python3", "run.py"]
