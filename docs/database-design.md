# Проектирование базы данных

## ER-диаграмма
users
id
username
email
password_hash
created_at

listings
id
user_id → users.id
title
description
game
price
is_exchange
exchange_for
image_url
created_at
is_completed


## SQL-скрипты

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    game TEXT NOT NULL,
    price REAL,
    is_exchange BOOLEAN DEFAULT 0,
    exchange_for TEXT,
    image_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_completed BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);