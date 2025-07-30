# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# It's good practice to install dependencies before copying the rest of the application
# to leverage Docker's layer caching.
RUN pip install --no-cache-dir gunicorn
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Expose the port that Gunicorn will listen on
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=main_clean.py
# IMPORTANT: Replace 'your_app_file.py' with your actual Flask application file

# Run Gunicorn to serve the Flask application
# The 'your_app_file:app' part should match your Flask application's entry point
# For example, if your Flask app is in 'app.py' and the Flask instance is named 'app', it would be 'app:app'
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "main_clean:app"]
# IMPORTANT: Replace your_app_file:app
