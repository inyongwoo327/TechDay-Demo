# Dockerfile
# Use an official Python runtime as a base image
FROM python:3.13.1-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the AWS default region
ENV AWS_ACCESS_KEY_ID=test
ENV AWS_SECRET_ACCESS_KEY=test
ENV AWS_REGION=eu-west-1
ENV S3_ENDPOINT=http://localstack:4566
ENV DYNAMODB_ENDPOINT=http://localstack:4566
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

COPY . .

# Expose the Flask port
EXPOSE 5000

# Run app.py when the container launches
CMD ["python3", "app.py"]
