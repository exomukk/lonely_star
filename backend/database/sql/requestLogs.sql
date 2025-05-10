CREATE TABLE request_logs (
    user_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    request_url TEXT,
    ip_address VARCHAR(45),
    geo_location TEXT,
    city VARCHAR(100)
);