FROM node:20-alpine

WORKDIR /app

# Copy CROD files
COPY crod-neural-network.js ./
COPY package.json ./

# Install dependencies
RUN npm install

# Copy startup script
COPY server.js ./

# Non-root user
RUN adduser -D crod
USER crod

EXPOSE 8100

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8100/health || exit 1

CMD ["node", "server.js"]