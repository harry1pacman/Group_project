from flask import Flask, request, jsonify
import sqlite3
import os 

app = Flask(__name__)

# Путь к базе данных
DATABASE = 'database.db'

# Создание базы данных и таблицы users
def init_db():
    if not os.path.exists(DATABASE):
        with app.app_context():
            db = sqlite3.connect(DATABASE)
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()

# Функция подключения к БД
def get_db():
    return sqlite3.connect(DATABASE)

# Роуты

# Регистрация пользователя
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Не все поля заполнены"}), 400

    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                       (username, email, password))  # В реальном приложении - используйте хэширование!
        db.commit()
        return jsonify({"message": "Пользователь успешно зарегистрирован"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email уже используется"}), 400

# Логин (упрощённый)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Введите email и пароль"}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, username FROM users WHERE email = ? AND password_hash = ?", (email, password))
    user = cursor.fetchone()

    if user:
        return jsonify({"message": "Вход выполнен", "user": {"id": user[0], "username": user[1]}}), 200
    else:
        return jsonify({"error": "Неверный email или пароль"}), 401

# Получение информации о пользователе
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, username, email, created_at FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if user:
        return jsonify({
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "created_at": user[3]
        }), 200
    else:
        return jsonify({"error": "Пользователь не найден"}), 404

# Схема базы данных
SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

# Создание файла базы данных и таблиц
def create_schema():
    with open('schema.sql', 'w') as f:
        f.write(SCHEMA)




# Роуты для объявлений

# Получить все объявления
@app.route('/listings', methods=['GET'])
def get_all_listings():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT id, user_id, title, description, game, price, is_exchange, exchange_for, image_url, created_at, is_completed
        FROM listings
    """)
    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "user_id": row[1],
            "title": row[2],
            "description": row[3],
            "game": row[4],
            "price": row[5],
            "is_exchange": bool(row[6]),
            "exchange_for": row[7],
            "image_url": row[8],
            "created_at": row[9],
            "is_completed": bool(row[10])
        })

    return jsonify(result), 200


# Получить одно объявление
@app.route('/listing/<int:listing_id>', methods=['GET'])
def get_listing(listing_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT id, user_id, title, description, game, price, is_exchange, exchange_for, image_url, created_at, is_completed
        FROM listings
        WHERE id = ?
    """, (listing_id,))
    row = cursor.fetchone()

    if row:
        return jsonify({
            "id": row[0],
            "user_id": row[1],
            "title": row[2],
            "description": row[3],
            "game": row[4],
            "price": row[5],
            "is_exchange": bool(row[6]),
            "exchange_for": row[7],
            "image_url": row[8],
            "created_at": row[9],
            "is_completed": bool(row[10])
        }), 200
    else:
        return jsonify({"error": "Объявление не найдено"}), 404


# Добавить новое объявление
@app.route('/listing', methods=['POST'])
def create_listing():
    data = request.get_json()
    user_id = data.get('user_id')
    title = data.get('title')
    description = data.get('description')
    game = data.get('game')
    price = data.get('price')
    is_exchange = data.get('is_exchange', False)
    exchange_for = data.get('exchange_for')
    image_url = data.get('image_url')

    if not all([user_id, title, description, game]):
        return jsonify({"error": "Не все обязательные поля заполнены"}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO listings 
        (user_id, title, description, game, price, is_exchange, exchange_for, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, title, description, game, price, is_exchange, exchange_for, image_url))

    db.commit()
    return jsonify({"message": "Объявление успешно добавлено", "id": cursor.lastrowid}), 20

@app.route('/listing/<int:listing_id>', methods=['PATCH'])
def update_listing(listing_id):
    data = request.get_json()
    is_completed = data.get('is_completed')

    if is_completed not in (0, 1):
        return jsonify({"error": "Неверное значение is_completed"}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE listings SET is_completed = ? WHERE id = ?", (is_completed, listing_id))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "Объявление не найдено"}), 404

    return jsonify({"message": "Статус обновлён", "is_completed": bool(is_completed)}), 200

# Запуск сервера
if __name__ == '__main__':
    create_schema()
    init_db()
    app.run(debug=True)