FROM python:3.11-slim

WORKDIR /app

# Install Node.js for Neural Bridge
RUN apt-get update && apt-get install -y nodejs npm && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY app.py .
COPY neural-bridge.js .
COPY crod-neural-network.js .
COPY package.json .
COPY start.sh .
RUN chmod +x start.sh

EXPOSE 7113

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:7113/health').raise_for_status()" || exit 1

CMD ["/app/start.sh"]