FROM python:3.13

WORKDIR /app

# Copy source code
COPY . .

# Install mkcert and dependencies
RUN apt-get update && apt-get install -y libnss3-tools curl

RUN curl -JLO https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-amd64 && \
    mv mkcert-v1.4.4-linux-amd64 /usr/local/bin/mkcert && chmod +x /usr/local/bin/mkcert

# Create local CA and domain certs
RUN mkcert -install && \
    mkcert -cert-file scamclubbe.creammjnk.uk.pem -key-file scamclubbe.creammjnk.uk-key.pem scamclubbe.creammjnk.uk

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["python", "database/nosql/insert_chests.py"]
CMD ["python", "app.py"]