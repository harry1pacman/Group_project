🗄️ Структура базы данных
Проект использует SQLite в качестве СУБД.
На начальном этапе реализованы две основные таблицы: users и listings.

1. Таблица users
Хранит информацию о зарегистрированных пользователях.

id
INTEGER PRIMARY KEY
Уникальный ID пользователя
username
TEXT NOT NULL
Логин пользователя
email
TEXT UNIQUE NOT NULL
Email пользователя (уникальный)
password_hash
TEXT NOT NULL
Хэшированный пароль пользователя
created_at
DATETIME DEFAULT CURRENT_TIMESTAMP
Дата регистрации

Пример SQL-запроса для создания:
sql


CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
⌄
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
2. Таблица listings
Содержит объявления пользователей на продажу или обмен игровых предметов.

id
INTEGER PRIMARY KEY
Уникальный ID объявления
user_id
INTEGER NOT NULL
Ссылка на пользователя (
users.id
)
title
TEXT NOT NULL
Название объявления
description
TEXT
Описание предмета
game
TEXT NOT NULL
Название игры
price
REAL
Цена (если продажа)
is_exchange
BOOLEAN DEFAULT 0
Возможен ли обмен
exchange_for
TEXT
На что готов обменяться
image_url
TEXT
Ссылка на изображение предмета
created_at
DATETIME DEFAULT CURRENT_TIMESTAMP
Дата публикации объявления
is_completed
BOOLEAN DEFAULT 0
Выполнено ли объявление

Пример SQL-запроса для создания:
sql


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
⌄
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
🔗 Связи между таблицами
Один ко многим: один пользователь может создать много объявлений.
Поле user_id в таблице listings ссылается на поле id в таблице users.
users.id → listings.user_id

1
users.id → listings.user_id
📐 ER-диаграмма (текстовое описание)
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