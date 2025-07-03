FROM node:20-alpine

WORKDIR /app

# Dependencies
COPY package*.json ./
RUN npm ci --only=production

# App files
COPY *.js ./

# Create non-root user
RUN adduser -D llama
USER llama

# Expose ports
EXPOSE 8089 8090

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8089/health || exit 1

CMD ["node", "server.js"]