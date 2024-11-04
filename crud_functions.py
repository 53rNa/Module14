import sqlite3

# Функция, которая создаёт таблицу Products, если она ещё не создана при помощи SQL запроса
def initiate_db():
    # Подключаемся к файлу базы данных products.db
    connection = sqlite3.connect('products.db')

    # Создаем объект курсора
    cursor = connection.cursor()

    # Выполняем запрос для создания таблицы Products
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
    )
    ''')
    # Сохраняем изменения
    connection.commit()

    # Закрываем соединение с базой данных
    connection.close()

# Функция, которая возвращает все записи из таблицы Products, полученные при помощи SQL запроса
def get_all_products():
    # Подключаемся к файлу базы данных products.db
    connection = sqlite3.connect('products.db')

    #  Создаем объект курсора
    cursor = connection.cursor()

    # Делаем выборку всех записей при помощи fetchall() из таблицы Products
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()

    # Закрываем соединение с базой данных
    connection.close()

    # Возвращаем полученный результат
    return products

# Пополняем таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота
def add_product(title, description, price):
    # Подключаемся к файлу базы данных products.db
    connection = sqlite3.connect('products.db')

    # Создаем объект курсора
    cursor = connection.cursor()

    # Добавляем записи в таблицу Products
    cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                   (title, description, price))

    # Сохраняем изменения
    connection.commit()

    # Закрываем соединение с базой данных
    connection.close()


# Функция для заполнения таблицы начальными данными
def populate_initial_data():
    products = [
        ("Продукт 1", "Описание 1", 100),
        ("Продукт 2", "Описание 2", 200),
        ("Продукт 3", "Описание 3", 300),
        ("Продукт 4", "Описание 4", 400)
    ]

    for product in products:
        add_product(*product)


# Инициализация базы данных и заполнение начальными данными
initiate_db()
populate_initial_data()
