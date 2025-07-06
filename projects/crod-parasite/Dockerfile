FROM python:3.11-alpine

# Install dependencies
RUN apk add --no-cache \
    build-base \
    git \
    sqlite

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy parasite code
COPY . .

# Create necessary directories
RUN mkdir -p /app/patterns /app/logs

# Expose ports
EXPOSE 7777 8765

# Start the parasite
CMD ["python", "crod_parasite_server.py"]