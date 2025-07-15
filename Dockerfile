# Use a lightweight official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install required system packages (Pillow dependencies)
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create the output directories if not present
RUN mkdir -p output/batch_qr output/student_qr

# Default command (can be overridden by docker-compose)
CMD ["python", "run_qr.py"]
