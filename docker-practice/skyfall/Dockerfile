# This line tells Docker to start with a pre-built Python environment
# Think of it like choosing a furnished apartment as your starting point
FROM python:3.10.13-slim

# These are like setting house rules - they configure how Python behaves
# PYTHONDONTWRITEBYTECODE=1 stops Python from creating .pyc files (compiled Python files)
# PYTHONUNBUFFERED=1 makes Python output appear immediately (useful for debugging)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# This sets the "home directory" inside the container where our app will live
# Like choosing which room in the apartment will be your office
WORKDIR /app

# Install system-level software that Django might need
# This is like installing utilities in your apartment (plumbing, electricity)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip (Python's package installer) to the latest version
# Like making sure you have the latest version of your toolbox
RUN pip install --upgrade pip

# Copy the requirements file into the container
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Create a non-root user for security (don't run as administrator)
# Like creating a regular user account instead of using the admin account
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Tell Docker that this container will use port 8000
# Like putting a sign on your apartment door saying "Office hours: Port 8000"
EXPOSE 8000

# The default command to run when the container starts
# Like setting your apartment to automatically turn on the lights when you enter
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Keep container running (recommended for development)
CMD ["tail", "-f", "/dev/null"]