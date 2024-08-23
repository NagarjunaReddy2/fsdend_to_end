FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /service

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . ./

# Define the command to run your application
ENTRYPOINT [ "python3", "app.py" ]
