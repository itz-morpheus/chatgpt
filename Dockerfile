FROM python:3.9-slim-buster  # Correct base image with one argument

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt /app/

# Update system and install necessary tools
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y git ffmpeg python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Specify the command to run the bot
CMD ["python3", "bot.py"]

