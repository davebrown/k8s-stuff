# Use an official Python runtime as a parent image
FROM python:2.7-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# pip install needs gcc
RUN apk add --no-cache gcc linux-headers musl-dev
# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
#EXPOSE 80
# Run app.py when the container launches
CMD ["python", "netcheck.py"]
