FROM elixir:1.14-alpine AS build

RUN apk add --no-cache build-base git python3

WORKDIR /app

RUN mix local.hex --force && \
    mix local.rebar --force

ENV MIX_ENV=prod

COPY mix.exs mix.lock ./
RUN mix deps.get --only $MIX_ENV
RUN mkdir config

COPY config/config.exs config/${MIX_ENV}.exs config/
RUN mix deps.compile

COPY lib lib
COPY priv priv

RUN mix compile

COPY config/runtime.exs config/

COPY rel rel
RUN mix release

FROM alpine:3.18 AS app
RUN apk add --no-cache openssl ncurses-libs libstdc++ ca-certificates

WORKDIR /app

RUN chown nobody:nobody /app

USER nobody:nobody

COPY --from=build --chown=nobody:nobody /app/_build/prod/rel/phoenix_rathaus ./

ENV HOME=/app

EXPOSE 4000

CMD ["bin/phoenix_rathaus", "start"]