CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    LUCKY_SEED VARCHAR(255) DEFAULT '',
    cash DECIMAL(10, 2) DEFAULT 0,
    role TEXT DEFAULT 'user' CHECK(role IN ('admin', 'user'))
);

SELECT * FROM user;