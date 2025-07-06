FROM node:18-alpine

WORKDIR /app

# Simple visualization server
RUN npm install -g http-server

COPY . .

EXPOSE 3000

CMD ["http-server", "-p", "3000"]