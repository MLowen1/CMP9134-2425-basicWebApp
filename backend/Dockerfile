# File: backend/Dockerfile

# Use a specific Debian release tag like 'bookworm' or 'bullseye'
FROM python:3.11-slim-bookworm

# Update OS packages to potentially patch base image vulnerabilities
# Run as root before potentially switching user
RUN apt-get update && apt-get upgrade -y && \
    # Clean up apt cache to reduce image size
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file first to leverage Docker build cache
COPY requirements.txt ./ 

# Install Python dependencies
# Using --no-cache-dir reduces image size
# Upgrading pip first is good practice
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of your backend application code into the WORKDIR (/app)
COPY . .

# Ensure Flask can find your modules. Usually not needed if WORKDIR is /app
# and FLASK_APP points correctly, but uncomment if you face import issues later.
# ENV PYTHONPATH=/app 

# Metadata indicating the port the container will listen on (doesn't actually publish it)
EXPOSE 5000 

# Command to run when the container starts:
# Uses Flask's built-in server via 'flask run'.
# --host=0.0.0.0 makes it listen on all container interfaces, necessary for port mapping.
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]