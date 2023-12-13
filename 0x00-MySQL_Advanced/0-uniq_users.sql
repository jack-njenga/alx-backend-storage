-- creates a table users that can be executed on any database
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT NOT NULL auto_increment PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);