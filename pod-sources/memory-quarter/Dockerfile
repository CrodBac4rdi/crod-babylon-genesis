FROM golang:1.20-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY *.go ./
RUN go build -o memory-quarter .

FROM alpine:latest
RUN apk --no-cache add ca-certificates

COPY --from=builder /app/memory-quarter /memory-quarter

EXPOSE 7031

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:7031/health || exit 1

CMD ["/memory-quarter"]