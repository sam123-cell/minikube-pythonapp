# Use a base Python image
FROM python:3.9.21-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY requirements.txt /app/

#install dependency
RUN pip install --no-cache-dir -r requirements.txt && pip install flask && pip install prometheus_client

#copy app file
COPY mysql_writer.py /app/
# Run the Python script
CMD ["python", "mysql_writer.py"]
