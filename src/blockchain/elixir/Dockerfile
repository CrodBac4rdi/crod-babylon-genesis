FROM elixir:1.15-alpine

# Install build dependencies
RUN apk add --no-cache build-base git

# Set working directory
WORKDIR /app

# Copy mix files
COPY mix.exs mix.lock ./

# Install dependencies
RUN mix local.hex --force && \
    mix local.rebar --force && \
    mix deps.get && \
    mix deps.compile

# Copy application code
COPY lib lib/
COPY config config/

# Compile application
RUN mix compile

# Build release
RUN mix release

# Expose port
EXPOSE 8000

# Start the application
CMD ["_build/prod/rel/crod/bin/crod", "start"]