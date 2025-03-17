# Use a base Python image
FROM python:3.9.21-slim

# Set working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt /app/
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && pip install flask && pip install prometheus_client
#copy app file
COPY mysql_reader.py /app/

# Run the Python script
CMD ["python", "mysql_reader.py"]
