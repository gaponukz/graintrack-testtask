DROP INDEX idx_products_subcategory_id;
DROP INDEX idx_subcategories_category_id;
DROP INDEX idx_completed_orders_product_id;

DROP TABLE completed_orders;
DROP TABLE reservations;
DROP TABLE customers;
DROP TABLE products;
DROP TABLE subcategories;
DROP TABLE categories;

DROP ROLE app;
