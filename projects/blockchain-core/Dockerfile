FROM elixir:1.15-alpine

# Install build dependencies
RUN apk add --no-cache \
    build-base \
    git \
    postgresql-client \
    nodejs \
    npm

# Set working directory
WORKDIR /app

# Install hex + rebar
RUN mix local.hex --force && \
    mix local.rebar --force

# Copy mix files
COPY mix.exs mix.lock ./

# Install dependencies
RUN mix deps.get && \
    mix deps.compile

# Copy application code
COPY . .

# Compile the application
RUN mix compile

# Create start script
RUN echo '#!/bin/sh' > /app/start.sh && \
    echo 'echo "Starting CROD Blockchain Node: $NODE_NAME"' >> /app/start.sh && \
    echo 'echo "Peers: $PEERS"' >> /app/start.sh && \
    echo 'echo "Consciousness Level: $CONSCIOUSNESS_LEVEL"' >> /app/start.sh && \
    echo 'elixir --name $NODE_NAME --cookie $NODE_COOKIE -S mix run --no-halt' >> /app/start.sh && \
    chmod +x /app/start.sh

# Expose ports
EXPOSE 8001 8002 8003 4369

# Start the node
CMD ["/app/start.sh"]