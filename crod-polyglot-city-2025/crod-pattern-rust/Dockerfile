FROM rust:1.75-alpine as builder

RUN apk add --no-cache musl-dev

WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src

RUN cargo build --release

FROM alpine:latest
RUN apk add --no-cache ca-certificates
COPY --from=builder /app/target/release/crod-pattern /usr/local/bin/

EXPOSE 7007

CMD ["crod-pattern"]
