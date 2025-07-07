FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Make script executable
RUN chmod +x crod_parasite_service.py

CMD ["python", "crod_parasite_service.py"]