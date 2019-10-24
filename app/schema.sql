DROP TABLE IF EXISTS groceries;
DROP TABLE IF EXISTS carts;
DROP TABLE IF EXISTS cart_groceries;
DROP TABLE IF EXISTS receipts;

CREATE TABLE groceries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  brand TEXT,
  price INTEGER NOT NULL DEFAULT 0,
  quantity INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
  updated_at TIMESTAMP NOT NULL DEFAULT current_timestamp
);

CREATE TABLE carts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  purchased INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
  updated_at TIMESTAMP NOT NULL DEFAULT current_timestamp
);

CREATE TABLE cart_groceries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cart_id INTEGER NOT NULL,
  grocery_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
  updated_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
  FOREIGN KEY (cart_id) REFERENCES cart(id),
  FOREIGN KEY (grocery_id) REFERENCES grocery(id),
  CONSTRAINT unique_cart_grocery UNIQUE (cart_id, grocery_id)
);

CREATE TABLE receipts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cart_id INTEGER NOT NULL,
  total_price INTEGER NOT NULL,
  paid_amount INTEGER NOT NULL,
  change_given INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
  updated_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
  FOREIGN KEY (cart_id) REFERENCES cart(id)
);
