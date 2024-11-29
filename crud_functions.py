import sqlite3

def initiate_db():
    connect = sqlite3.connect('products.db')
    cursor = connect.cursor()

    connect2 = sqlite3.connect('users.db')
    cursor2 = connect2.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    );
    ''')

    cursor2.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INT NOT NULL,
    balance INT NOT NULL DEFAULT 1000
    );
    ''')

    for i in range(1, 5):
        cursor.execute("INSERT INTO Products(id, title, description, price) VALUES(?, ?, ?, ?)",
                       (i, f'Продукт{i}', f'Описание{i}', f'{i * 100}'))
    connect.commit()
    connect.close()
    connect2.commit()
    connect2.close()

def get_all_products():
    connect = sqlite3.connect('products.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connect.commit()
    connect.close()
    return products

def add_user(username, email, age):
    connect2 = sqlite3.connect('users.db')
    cursor2 = connect2.cursor()
    cursor2.execute("INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)",
                   (f'{username}', f'{email}', f'{age}', 1000))
    connect2.commit()
    connect2.close()

def is_included(username):
    connect2 = sqlite3.connect('users.db')
    cursor2 = connect2.cursor()
    user = cursor2.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
    connect2.commit()
    connect2.close()
    return user is not None