CREATE DATABASE IF NOT EXISTS atm_db;

USE atm_db;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    balance DECIMAL(15, 2) DEFAULT 0.00,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Banknotes table
CREATE TABLE IF NOT EXISTS banknotes (
    denomination INT PRIMARY KEY,
    quantity INT NOT NULL DEFAULT 0
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    transaction_type ENUM('deposit', 'withdrawal', 'transfer_sent', 'transfer_received', 'pin_change') NOT NULL,
    amount DECIMAL(15, 2),
    recipient_id INT,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (recipient_id) REFERENCES users(user_id)
);

-- Insert initial banknotes
INSERT INTO banknotes (denomination, quantity) VALUES 
(500000, 100),
(200000, 100),
(100000, 100),
(50000, 100),
(20000, 100),
(10000, 100)
ON DUPLICATE KEY UPDATE quantity = VALUES(quantity);

-- Insert admin user (password is 'admin123')
INSERT INTO users (username, password, full_name, is_admin) VALUES 
('admin', 'admin123', 'Administrator', TRUE)
ON DUPLICATE KEY UPDATE password = VALUES(password);