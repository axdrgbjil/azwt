# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# If you have a requirements.txt file, uncomment and use this line
# RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that your app will run on (12345)
EXPOSE 12345

# Set a default environment variable (optional but good for container identification)
ENV PYTHONUNBUFFERED=1

# Install any necessary dependencies (if you have any)
RUN pip install --no-cache-dir

# Command to run the application
ENTRYPOINT ["python3", "run.py"]

# Optional: Add healthcheck to make sure the app is alive and well
# HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
#   CMD nc -zv 127.0.0.1 12345 || exit 1
