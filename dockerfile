# 1. Use an official Python runtime as a parent image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the essential files into the container
COPY main.py /app/
COPY Modules/ /app/Modules/

# 4. Create a volume for the logfile
VOLUME ["/app/logfile"]
VOLUME ["/app/order_data"]

# 5. Install any necessary Python packages (adjust this if you have a requirements.txt)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Install Gunicorn
RUN pip install gunicorn

# 7. Expose the Flask port (default 5000)
EXPOSE 5000

# 8. Command to run the application with Gunicorn and log configuration
CMD ["python", "main.py"]
