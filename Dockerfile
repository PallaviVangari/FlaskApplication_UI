# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in docker
WORKDIR /app

# Copy the content of the local src directory to the working directory
COPY . /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run ui_service.py when the container launches
CMD ["python", "ui_service.py"]
