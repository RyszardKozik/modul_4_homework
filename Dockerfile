# Use the Python base image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy all other files into the container
COPY . .

# Check if the storage directory and data.json file exist, if not, create them
RUN mkdir -p storage && touch storage/data.json

# Expose port 5500 to allow external access
EXPOSE 5500

# Run the application when the container starts
CMD ["python", "app.py"]