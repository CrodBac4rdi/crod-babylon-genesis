FROM elixir:1.16-alpine AS build

# Install build dependencies
RUN apk add --no-cache build-base git python3

# Prepare build dir
WORKDIR /app

# Install hex + rebar
RUN mix local.hex --force && \
    mix local.rebar --force

# Set build ENV
ENV MIX_ENV=prod

# Install mix dependencies
COPY mix.exs mix.lock ./
RUN mix deps.get --only $MIX_ENV
RUN mkdir config

# Copy compile-time config files
COPY config/config.exs config/${MIX_ENV}.exs config/
RUN mix deps.compile

# Copy application files
COPY lib lib/
COPY priv priv/

# Compile and build release
RUN mix compile

# Start a new build stage for runtime
FROM alpine:3.19 AS app

RUN apk add --no-cache openssl ncurses-libs libstdc++ libgcc

WORKDIR /app

# Install hex + rebar for runtime
RUN apk add --no-cache elixir
RUN mix local.hex --force && \
    mix local.rebar --force

# Copy the application
COPY --from=build /app /app

# Set runtime ENV
ENV MIX_ENV=prod

EXPOSE 4000

CMD ["mix", "phx.server"]