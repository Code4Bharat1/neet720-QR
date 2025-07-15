FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libjpeg-dev zlib1g-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p output/batch_qr output/student_qr

CMD ["python", "run_qr.py"]
