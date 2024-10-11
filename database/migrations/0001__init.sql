CREATE ROLE app WITH LOGIN;

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE subcategories (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL,
    name text NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    subcategory_id INTEGER NOT NULL,
    name text NOT NULL,
    price double precision NOT NULL,
    available INTEGER NOT NULL,
    reserved INTEGER NOT NULL,
    discount INTEGER NOT NULL,
    FOREIGN KEY (subcategory_id) REFERENCES subcategories(id)
);

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE reservations (
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (customer_id, product_id),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE completed_orders (
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (customer_id, product_id),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE INDEX idx_subcategories_category_id ON subcategories (category_id);
CREATE INDEX idx_products_subcategory_id ON products (subcategory_id);

GRANT SELECT ON TABLE categories TO app;
GRANT SELECT ON TABLE subcategories TO app;
GRANT SELECT,INSERT ON TABLE products TO app;
GRANT UPDATE(price) ON TABLE products TO app;
GRANT UPDATE(discount) ON TABLE products TO app;
GRANT UPDATE(available) ON TABLE products TO app;
GRANT UPDATE(reserved) ON TABLE products TO app;
GRANT USAGE ON SEQUENCE products_id_seq TO app;
GRANT DELETE ON TABLE products TO app;
GRANT SELECT ON TABLE customers TO app;
GRANT SELECT,INSERT ON TABLE reservations TO app;
GRANT DELETE ON TABLE reservations TO app;
GRANT SELECT,INSERT ON TABLE completed_orders TO app;
