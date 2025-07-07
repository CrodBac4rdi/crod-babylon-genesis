FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY parasit.py .

# Create non-root user
RUN useradd -m -u 1000 crod && chown -R crod:crod /app
USER crod

EXPOSE 6666

CMD ["python", "parasit.py"]