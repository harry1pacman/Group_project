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

# Запуск сервера
if __name__ == '__main__':
    create_schema()
    init_db()
    app.run(debug=True)