-- Initialize the spotbot database schema
CREATE TABLE IF NOT EXISTS spots (
    callsign VARCHAR(20) PRIMARY KEY,
    message_id VARCHAR(100) NOT NULL,
    utctimestamp DATETIME NOT NULL,
    INDEX idx_utctimestamp (utctimestamp)
);
