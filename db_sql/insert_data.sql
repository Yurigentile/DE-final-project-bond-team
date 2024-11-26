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