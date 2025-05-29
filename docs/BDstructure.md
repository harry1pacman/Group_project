Это документ описывает структуру базы данных проекта "Игровой маркетплейс" — веб-платформы для продажи и обмена игровыми предметами. 

📁 Таблицы
1. users — пользователи платформы
![Таблица БД пользователи платформы.png](%D0%A2%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20%D0%91%D0%94%20%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D0%B8%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D1%8B.png)
2. listings — объявления
![Таблица БД Объявления.png](%D0%A2%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20%D0%91%D0%94%20%D0%9E%D0%B1%D1%8A%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F.png)


🔗 Связи между таблицами
users.id → listings.user_id
(один ко многим)

🧩 ER-диаграмма (текстовое описание)
users
-----
id
username
email
password_hash
created_at

listings
--------
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

🧾 Пример SQL-скрипта для создания таблиц
-- Создание таблицы пользователей
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы объявлений
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