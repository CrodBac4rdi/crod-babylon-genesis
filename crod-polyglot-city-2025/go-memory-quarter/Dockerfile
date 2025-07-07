# Build stage
FROM golang:1.21-alpine AS builder

RUN apk add --no-cache git

WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY main.go .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o crod-memory-quarter .

# Runtime stage
FROM alpine:3.18

RUN apk add --no-cache ca-certificates

WORKDIR /app

# Copy the binary from builder
COPY --from=builder /app/crod-memory-quarter .

# Create directory for BadgerDB
RUN mkdir -p /tmp/crod-memory

# Create non-root user
RUN adduser -D -u 1000 crod && chown -R crod:crod /app /tmp/crod-memory
USER crod

EXPOSE 7031

CMD ["./crod-memory-quarter"]