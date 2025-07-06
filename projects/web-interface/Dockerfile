FROM elixir:1.15-alpine

# Install build dependencies and nodejs for assets
RUN apk add --no-cache \
    build-base \
    git \
    nodejs \
    npm \
    inotify-tools

WORKDIR /app

# Install hex + rebar + phoenix
RUN mix local.hex --force && \
    mix local.rebar --force && \
    mix archive.install hex phx_new --force

# Copy mix files
COPY mix.exs mix.lock* ./

# Install dependencies
RUN mix deps.get && \
    mix deps.compile

# Copy application
COPY . .

# Install node dependencies for assets
RUN cd assets && npm install

# Compile assets
RUN mix assets.deploy

# Expose Phoenix port
EXPOSE 4000

CMD ["mix", "phx.server"]