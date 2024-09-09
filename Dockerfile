# Use python:3.9-slim as the base image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install the dependencies using pip
RUN pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Set the command to run the Flask app
CMD ["python", "spotbot.py"]
