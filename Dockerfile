# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the dependencies from the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that your app will run on (12345)
EXPOSE 12345

# Set a default environment variable (optional but good for container identification)
ENV PYTHONUNBUFFERED=1

# Command to run the application
ENTRYPOINT ["python3", "run.py"]
