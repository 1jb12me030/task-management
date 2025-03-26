# Use the official Python 3.10 image
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install SQLite and dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    sqlite3 libsqlite3-dev && \
    rm -rf /var/lib/apt/lists/*

# Verify SQLite installation
RUN sqlite3 --version
COPY db.sqlite3 /app/db.sqlite3

# Copy the project files to the container
COPY . /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the port for Django
EXPOSE 8000

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]

