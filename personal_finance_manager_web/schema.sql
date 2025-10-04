CREATE DATABASE IF NOT EXISTS finance_manager;
USE finance_manager;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_Name VARCHAR(100),
    last_Name VARCHAR(100),
    Username VARCHAR(100) UNIQUE,
    Password VARCHAR(255),
    birthday DATE,
    Occupation VARCHAR(100),
    Location VARCHAR(100),
    balance DECIMAL(10,2) DEFAULT 0.00
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10, 2),
    type VARCHAR(10),
    category VARCHAR(100),
    description TEXT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS savings_goals (
    goal_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    goal_name VARCHAR(100),
    target_amount DECIMAL(10, 2),
    saved_amount DECIMAL(10, 2),
    deadline DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS budgets (
    budget_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    category VARCHAR(100),
    amount DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
