# Build stage
FROM elixir:1.15-alpine AS build

RUN apk add --no-cache build-base git

WORKDIR /app

# Install hex + rebar
RUN mix local.hex --force && \
    mix local.rebar --force

# Set build ENV
ENV MIX_ENV=prod

# Install mix dependencies
COPY mix.exs mix.lock ./
RUN mix deps.get --only $MIX_ENV
RUN mix deps.compile

# Copy app files
COPY lib lib/
COPY config config/

# Compile and build release
RUN mix compile
RUN mix release

# Runtime stage
FROM alpine:3.18 AS runtime

RUN apk add --no-cache openssl ncurses-libs libstdc++ libgcc

WORKDIR /app

# Copy release from build stage
COPY --from=build /app/_build/prod/rel/crod_rathaus ./

ENV HOME=/app
ENV PORT=4000

EXPOSE 4000

CMD ["bin/crod_rathaus", "start"]