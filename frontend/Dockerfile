FROM node:20

WORKDIR /app

COPY . .

RUN npm install

# Build your React app
RUN npm run build

# Serve with HTTPS using `serve` package (good for local/prod static)
RUN npm install -g serve

# Optional: Use mkcert to create HTTPS cert
RUN apt-get update && apt-get install -y libnss3-tools curl && \
    curl -JLO https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-amd64 && \
    mv mkcert-v1.4.4-linux-amd64 /usr/local/bin/mkcert && chmod +x /usr/local/bin/mkcert && \
    mkcert -install && \
    mkcert -cert-file localhost.pem -key-file localhost-key.pem localhost

# Expose HTTPS port
EXPOSE 3000

# Serve built app using HTTPS
CMD ["serve", "-s", "build", "--ssl-cert", "localhost.pem", "--ssl-key", "localhost-key.pem", "-l", "3000"]