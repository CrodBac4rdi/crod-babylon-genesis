FROM ollama/ollama:latest

# CROD LLAMA District - Secure AI Processing
LABEL maintainer="CROD System"
LABEL description="LLAMA District - Local AI with CROD Integration"

# Create crod user for security
RUN useradd -m -s /bin/bash crod

# Setup directories
RUN mkdir -p /home/crod/models /home/crod/data /home/crod/app && \
    chown -R crod:crod /home/crod

# Copy application files
WORKDIR /home/crod/app
COPY --chown=crod:crod llama-server.py ./
COPY --chown=crod:crod requirements.txt ./
COPY --chown=crod:crod crod-llama-modelfile ./Modelfile

# Install Python for API server
RUN apt-get update && apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
USER crod
RUN pip3 install --user -r requirements.txt

# Create CROD-LLAMA model
USER root
RUN ollama serve & sleep 5 && \
    ollama create crod-llama -f ./Modelfile && \
    pkill ollama

# Switch to crod user
USER crod

# Expose port (internal only!)
EXPOSE 7777

# Start both ollama and API server
CMD ["sh", "-c", "ollama serve & python3 llama-server.py"]