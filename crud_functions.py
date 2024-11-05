import sqlite3

# Функция, которая создаёт таблицу Products, если она ещё не создана при помощи SQL запроса
def initiate_db():
    try:
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


        # Выполняем запрос для создания таблицы Users
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL DEFAULT 1000
        )
        ''')


        # Сохраняем изменения
        connection.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при инициализации базы данных: {e}")

    finally:
        if connection:
            # Закрываем соединение с базой данных
            connection.close()


# Функция, которая возвращает все записи из таблицы Products, полученные при помощи SQL запроса
def get_all_products():
    try:
        # Подключаемся к файлу базы данных products.db
        connection = sqlite3.connect('products.db')

        #  Создаем объект курсора
        cursor = connection.cursor()

        # Делаем выборку всех записей при помощи fetchall() из таблицы Products
        cursor.execute('SELECT * FROM Products')
        products = cursor.fetchall()

        # Возвращаем полученный результат
        return products
    except sqlite3.Error as e:
        print(f"Ошибка при получении всех продуктов: {e}")
        return []
    finally:
        if connection:
            # Закрываем соединение с базой данных
            connection.close()




# Пополняем таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота
def add_product(title, description, price):
    try:
        # Подключаемся к файлу базы данных products.db
        connection = sqlite3.connect('products.db')

        # Создаем объект курсора
        cursor = connection.cursor()

        # Добавляем записи в таблицу Products
        cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                       (title, description, price))

        # Сохраняем изменения
        connection.commit()

    except sqlite3.Error as e:
        print(f"Ошибка при добавлении продукта: {e}")
    finally:
        if connection:
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


# Функция для добавления нового пользователя
def add_user(username, email, age):
    try:
        connection = sqlite3.connect('products.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)',
                       (username, email, age))
        connection.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")
    finally:
        if connection:
            connection.close()


# Функция для проверки на наличие пользователя
def is_included(username):
    try:
        connection = sqlite3.connect('products.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
        user = cursor.fetchone()
        return user is not None
    except sqlite3.Error as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return False
    finally:
        if connection:
            connection.close()



# Инициализация базы данных и заполнение начальными данными
initiate_db()
populate_initial_data()
