import sqlite3
conn = sqlite3.connect("pizzeria.db")
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()
cur.executescript("""
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS products;
""")
cur.execute("""
CREATE TABLE users (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  TEXT NOT NULL,
    phone TEXT UNIQUE
)
""")
cur.execute("""
CREATE TABLE products (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price INTEGER
)
""")
cur.execute("""
CREATE TABLE orders (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER,
    product_id INTEGER,
    quantity   INTEGER DEFAULT 1,
    FOREIGN KEY (user_id)    REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
)
""")
cur.executemany("INSERT INTO users (name, phone) VALUES (?, ?)", [
    ("Алексей", "+998901111111"),
    ("Мария",   "+998902222222"),
    ("Дмитрий", "+998903333333"),
])
cur.executemany("INSERT INTO products (title, price) VALUES (?, ?)", [
    ("Маргарита",   500),
    ("Пепперони",   650),
    ("Четыре сыра", 700),
    ("Гавайская",   600),
])
cur.executemany("INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)", [
    (1, 1, 2),
    (1, 3, 1),
    (2, 2, 3),
    (3, 4, 1),
    (2, 1, 1),
])
conn.commit()
print("5-topshiriq: Barcha buyurtmalar")
cur.execute("""
SELECT users.name, products.title, orders.quantity
FROM orders
INNER JOIN users    ON orders.user_id    = users.id
INNER JOIN products ON orders.product_id = products.id
""")
print(f"{'Mijoz':<10}{'Pitsa':<15}{'Soni':>5}")
for name, title, qty in cur.fetchall():
    print(f"{name:<10}{title:<15}{qty:>5}")
print("\n6-topshiriq: Umumiy narx bilan, qimmatdan arzonga")
cur.execute("""
SELECT users.name, products.title, orders.quantity,
       products.price * orders.quantity AS total
FROM orders
INNER JOIN users    ON orders.user_id    = users.id
INNER JOIN products ON orders.product_id = products.id
ORDER BY total DESC
""")
print(f"{'Mijoz':<10}{'Pitsa':<15}{'Soni':>5}{'Jami':>8}")
for name, title, qty, total in cur.fetchall():
    print(f"{name:<10}{title:<15}{qty:>5}{total:>8}")

conn.close()
