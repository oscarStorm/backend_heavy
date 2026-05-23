CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS resources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    capacity INT,
    tablename VARCHAR(255),
    active BOOL NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT NOT NULL,
    resource_id INT NOT NULL,

    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (resource_id) REFERENCES resources(id),

    CHECK (end_time > start_time)
);
