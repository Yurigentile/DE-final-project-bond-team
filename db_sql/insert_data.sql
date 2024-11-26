INSERT INTO users (name, email) VALUES
('Alice', 'alice@example.com'),
('Bob', 'bob@example.com'),
('Charlie', 'charlie@example.com');

-- Insert products
INSERT INTO products (name, price) VALUES
('Laptop', 999.99),
('Mouse', 19.99),
('Keyboard', 49.99),
('Monitor', 199.99),
('Headphones', 89.99);

-- Insert orders
INSERT INTO orders (user_id, order_date) VALUES
(1, '2024-11-20'),
(2, '2024-11-21'),
(3, '2024-11-22');

-- Insert order items
INSERT INTO order_items (order_id, product_id, quantity) VALUES
(1, 1, 1), -- Alice ordered 1 Laptop
(1, 2, 2), -- Alice ordered 2 Mice
(2, 3, 1), -- Bob ordered 1 Keyboard
(3, 4, 1), -- Charlie ordered 1 Monitor
(3, 5, 3); -- Charlie ordered 3 Headphones

-- Insert reviews
INSERT INTO reviews (user_id, product_id, rating, comment) VALUES
(1, 1, 5, 'Great laptop!'),
(1, 2, 4, 'The mouse is good but could be better.'),
(2, 3, 3, 'Average keyboard.'),
(3, 4, 5, 'Love the monitor! Crystal clear.'),
(3, 5, 4, 'Headphones are solid.');

INSERT INTO design (design_id, created_at, design_name, file_location, file_name, last_updated) VALUES
(472, '2024-11-14T09:41:09.839000', 'Concrete', '/usr/share', 'concrete-20241026-76vi.json', '2024-11-14T09:41:09.839000'),
(473, '2024-11-15T14:09:09.608000', 'Rubber', '/Users', 'rubber-20240916-1hsu.json', '2024-11-15T14:09:09.608000');

INSERT INTO sales_order (sales_order_id, created_at, last_updated, design_id, staff_id, counterparty_id, units_sold, unit_price, currency_id, agreed_delivery_date, agreed_payment_date, agreed_delivery_location_id) VALUES
(11165, '2024-11-14T10:19:09.990000', '2024-11-14T10:19:09.990000', 472, 18, 19, 12145, 3.83, 3, '2024-11-15', '2024-11-15', 26),
(11166, '2024-11-14T11:36:10.342000', '2024-11-14T11:36:10.342000', 473, 14, 20, 75609, 3.52, 3, '2024-11-15', '2024-11-20', 7);
