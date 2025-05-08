CREATE TABLE request_logs (
    user_id INT NOT NULL,
    request_time DATETIME,
    request_url TEXT,
    ip_address VARCHAR(45),
    geo_location TEXT,
    city VARCHAR(100)
);