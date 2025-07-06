FROM python:3.11-alpine

# Install dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    g++

WORKDIR /app

# Install Python packages
RUN pip install --no-cache-dir \
    flask \
    redis \
    psycopg2-binary \
    requests \
    numpy

# Copy application
COPY crod_parasite.py .

# Expose ports
EXPOSE 7777 8888

# Run the parasite
CMD ["python", "crod_parasite.py"]