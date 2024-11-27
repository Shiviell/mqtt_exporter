FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your Python scripts into the container
COPY . /app/
#COPY setup.py /app/

# Install any necessary dependencies (if needed)
RUN pip install -r requirements.txt

# Run server
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
