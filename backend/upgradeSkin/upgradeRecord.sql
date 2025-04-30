CREATE TABLE upgraderoom (
    userId VARCHAR(50) NOT NULL,
    userWeaponId VARCHAR(50) NOT NULL,
    expectedWeaponId VARCHAR(50) NOT NULL,
    successRate INT NOT NULL,
    upgradeDate TIMESTAMP,
    success BOOLEAN           DEFAULT FALSE
);