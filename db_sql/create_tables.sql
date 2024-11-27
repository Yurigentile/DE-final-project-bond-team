-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100)
);

-- Products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10, 2)
);

-- Orders table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    order_date DATE DEFAULT CURRENT_DATE
);

-- Order Items table
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id) ON DELETE CASCADE,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    quantity INT
);

-- Reviews table
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT
);

CREATE TABLE design (
    design_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    design_name VARCHAR NOT NULL,
    file_location VARCHAR NOT NULL,
    file_name VARCHAR NOT NULL
);

CREATE TABLE currency (
    currency_id SERIAL PRIMARY KEY,
    currency_code VARCHAR(3) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sales_order (
    sales_order_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    design_id INT NOT NULL REFERENCES design(design_id),
    staff_id INT NOT NULL, --REFERENCES staff(staff_id),
    counterparty_id INT NOT NULL, --REFERENCES counterparty(counterparty_id),
    units_sold INT NOT NULL CHECK (units_sold BETWEEN 1000 AND 100000),
    unit_price NUMERIC NOT NULL CHECK (unit_price BETWEEN 2.00 AND 4.00),
    currency_id INT NOT NULL, --REFERENCES currency(currency_id),
    agreed_delivery_date VARCHAR NOT NULL,
    agreed_payment_date VARCHAR NOT NULL,
    agreed_delivery_location_id INT NOT NULL --REFERENCES address(address_id)
);

CREATE TABLE staff (
    staff_id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    department_id INT NOT NULL, --REFERENCES department(department_id),
    email_address VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE counterparty (
    counterparty_id SERIAL PRIMARY KEY,
    counterparty_legal_name VARCHAR NOT NULL,
    legal_address_id INT NOT NULL , --REFERENCES address(address_id),
    commercial_contact VARCHAR,
    delivery_contact VARCHAR,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE address (
    address_id SERIAL PRIMARY KEY,
    address_line_1 VARCHAR NOT NULL,
    address_line_2 VARCHAR,
    district VARCHAR,
    city VARCHAR NOT NULL,
    postal_code VARCHAR NOT NULL,
    country VARCHAR NOT NULL,
    phone VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE department (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR NOT NULL,
    "location" VARCHAR,
    manager VARCHAR,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE purchase_order (
    purchase_order_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    staff_id INT NOT NULL, --REFERENCES staff(staff_id),
    counterparty_id INT NOT NULL, --REFERENCES counterparty(counterparty_id),
    item_code VARCHAR NOT NULL,
    item_quantity INT NOT NULL CHECK (item_quantity BETWEEN 1 AND 1000),
    item_unit_price NUMERIC NOT NULL CHECK (item_unit_price BETWEEN 3 AND 1000),
    currency_id INT NOT NULL, --REFERENCES currency(currency_id),
    agreed_delivery_date VARCHAR NOT NULL,
    agreed_payment_date VARCHAR NOT NULL,
    agreed_delivery_location_id INT NOT NULL --REFERENCES address(address_id)
);

CREATE TABLE payment_type (
    payment_type_id SERIAL PRIMARY KEY,
    payment_type_name VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payment (
    payment_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    transaction_id INT NOT NULL, --REFERENCES transaction(transaction_id),
    counterparty_id INT NOT NULL, --REFERENCES counterparty(counterparty_id),
    payment_amount NUMERIC NOT NULL CHECK (payment_amount BETWEEN 1 AND 1000000),
    currency_id INT NOT NULL, --REFERENCES currency(currency_id),
    payment_type_id INT NOT NULL, --REFERENCES payment_type(payment_type_id),
    paid BOOLEAN NOT NULL,
    payment_date VARCHAR NOT NULL,
    company_ac_number INT NOT NULL CHECK (company_ac_number BETWEEN 10000000 AND 99999999),
    counterparty_ac_number INT NOT NULL CHECK (counterparty_ac_number BETWEEN 10000000 AND 99999999)
);

CREATE TABLE transaction (
    transaction_id SERIAL PRIMARY KEY,
    transaction_type VARCHAR NOT NULL,
    sales_order_id INT, --REFERENCES sales_order(sales_order_id),
    purchase_order_id INT, --REFERENCES purchase_order(purchase_order_id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


