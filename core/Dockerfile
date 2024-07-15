# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY ../requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from the parent directory into the container
COPY .. .

# Make run.sh executable (ensure correct path)
RUN chmod +x /app/run.sh

# Expose port if needed
EXPOSE 80

# Set the command to run your script
CMD ["/app/run.sh"]
