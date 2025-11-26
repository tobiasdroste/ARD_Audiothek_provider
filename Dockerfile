# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the file from your host to your current location.
COPY pyproject.toml .
COPY app.py .
COPY README.md .

# Install dependencies
# We use pip to install the project and its dependencies directly from pyproject.toml
RUN pip install --no-cache-dir .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
