FROM elixir:1.15-alpine AS build

# Install build dependencies
RUN apk add --no-cache build-base npm git python3 postgresql-client

# Install hex + rebar
RUN mix local.hex --force && \
    mix local.rebar --force

ENV MIX_ENV=prod

WORKDIR /app

# Install mix dependencies
COPY mix.exs mix.lock ./
RUN mix deps.get --only $MIX_ENV
RUN mkdir config

# Copy compile-time config files
COPY config/config.exs config/${MIX_ENV}.exs config/
RUN mix deps.compile

# Copy assets
COPY assets assets/

# Compile assets
RUN mix assets.deploy

# Compile project
COPY lib lib/
COPY priv priv/
RUN mix compile

# Create release
COPY config/runtime.exs config/
RUN mix release

# Final stage
FROM alpine:3.19 AS app

RUN apk add --no-cache libstdc++ openssl ncurses-libs postgresql-client

WORKDIR /app

RUN chown nobody:nobody /app

USER nobody:nobody

COPY --from=build --chown=nobody:nobody /app/_build/prod/rel/crod_rathaus ./

ENV HOME=/app
ENV PHX_SERVER=true
ENV PORT=4000

EXPOSE 4000

CMD ["bin/crod_rathaus", "start"]