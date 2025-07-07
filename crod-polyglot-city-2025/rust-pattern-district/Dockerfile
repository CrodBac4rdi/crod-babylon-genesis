# Build stage
FROM rust:1.75-alpine AS builder

RUN apk add --no-cache musl-dev

WORKDIR /app

# Copy manifest files
COPY Cargo.toml Cargo.lock ./

# Create dummy main.rs for dependency caching
RUN mkdir src && echo "fn main() {}" > src/main.rs

# Build dependencies
RUN cargo build --release
RUN rm -rf src

# Copy source code
COPY src ./src

# Build the application
RUN touch src/main.rs && cargo build --release

# Runtime stage
FROM alpine:3.18

RUN apk add --no-cache libgcc

WORKDIR /app

# Copy the binary from builder
COPY --from=builder /app/target/release/crod-pattern-district /app/

# Create non-root user
RUN adduser -D -u 1000 crod
USER crod

EXPOSE 7007

CMD ["./crod-pattern-district"]