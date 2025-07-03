FROM node:20-alpine

WORKDIR /app

# Dependencies
COPY package*.json ./
RUN npm ci --only=production

# App
COPY webhook.js ./

# Security - non-root user
USER node

EXPOSE 8086

CMD ["node", "webhook.js"]