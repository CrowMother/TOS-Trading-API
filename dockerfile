# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

RUN pip install --upgrade pip
# Install any Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Expose the port the app runs on
EXPOSE 80

# Define environment variables (optional)
ENV SERVER_URL="http://nobelltrading.duckdns.org/trades"

# Run the Flask application
CMD ["python", "main.py"]
