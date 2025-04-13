# Sử dụng Node.js image làm base
FROM node:14-alpine

# Cài đặt Snyk CLI
RUN npm install -g snyk

# Copy token (hoặc set token qua biến môi trường khi build)
ENV SNYK_TOKEN=e03deb41-76e1-4872-9e62-156c461f9359

# Tạo thư mục làm việc trong container
WORKDIR /app
COPY /frontend /app

# Lệnh mặc định để chạy khi container bắt đầu: quét bảo mật Snyk
CMD ["snyk", "test"]
