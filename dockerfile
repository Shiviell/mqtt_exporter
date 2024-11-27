FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your Python scripts into the container
COPY . /app/
#COPY setup.py /app/

# Install any necessary dependencies (if needed)
RUN pip install -r requirements.txt

# Run server
CMD ["python3", "server.py"]
