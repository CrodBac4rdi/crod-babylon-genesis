FROM node:18-alpine

WORKDIR /app

# Copy files
COPY package.json .
COPY neural-bridge.js .
COPY crod-neural-network.js .

# Install deps
RUN npm install

EXPOSE 9999

CMD ["node", "neural-bridge.js"]