# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8008

# Define environment variable
ENV NAME World
#ENV DB_HOST 10.0.2.2 # hack, based on minikube behavior: https://github.com/kubernetes/minikube/issues/352
ENV DB_HOST 127.0.0.1
# Run app.py when the container launches
CMD ["python", "counter.py"]
