# Sử dụng Node.js image làm base
FROM node:14-alpine

# Cài đặt Python và pip
RUN apk add --no-cache python3 py3-pip

# Cài đặt Snyk CLI
RUN npm install -g snyk && snyk --version

# Chỉ dùng để debug, có thể bỏ qua
RUN echo $SNYK_TOKEN  

# Cài đặt Flask và các thư viện cần thiết cho Python
RUN pip install Flask

# Định nghĩa ARG để nhận giá trị SNYK_TOKEN từ khi build
ARG SNYK_TOKEN

# Copy token (hoặc set token qua biến môi trường khi build)
ENV SNYK_TOKEN=${SNYK_TOKEN}

# Tạo thư mục làm việc trong container
WORKDIR /app
COPY . /app

# Quét bảo mật mã nguồn và thư viện phụ thuộc
# RUN snyk test --all-projects --json || echo "Snyk test failed"
RUN snyk test --all-projects --json | tee ./snyk-results.json

# Cấu hình web server Flask
CMD ["python", "snyk.py"]
