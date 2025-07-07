FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application files
COPY index.js .

# Create non-root user
RUN adduser -D -u 1000 crod && chown -R crod:crod /app
USER crod

EXPOSE 7888

CMD ["node", "index.js"]