FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

EXPOSE 7113

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:7113/health').raise_for_status()" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:7113", "--workers", "2", "--threads", "4", "app:app"]