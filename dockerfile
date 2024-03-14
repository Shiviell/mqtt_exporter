FROM python:3

# Install supervisor
RUN apt-get update && apt-get install -y supervisor

# Set the working directory inside the container
WORKDIR /app

# Copy your Python scripts into the container
COPY . /app/
#COPY setup.py /app/

# Install any necessary dependencies (if needed)
RUN pip install -r requirements.txt

# Configure supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Run supervisord
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
