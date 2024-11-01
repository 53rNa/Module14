# Задача "Первые пользователи"

import sqlite3

# Подключаемся к файлу базы данных not_telegram.db
connection = sqlite3.connect('not_telegram.db')

# Создаем объект курсора
cursor = connection.cursor()

# Выполняем запрос для создания таблицы Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

# Выполняем вставку в таблицу Users данных о 10-ти пользователях
for i in range(1, 11):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (f"User{i}", f"example{i}@gmail.com", i*10, "1000"))

# Обновляем balance у каждой 2-ой записи начиная с 1-ой на 500
cursor.execute('''
UPDATE Users
SET balance = 500
WHERE id IN (SELECT id FROM Users WHERE id % 2 = 1)
''')

# Удаляем каждую 3-ю запись в таблице начиная с 1-ой
cursor.execute('''
DELETE FROM Users
WHERE id IN (SELECT id FROM Users WHERE id % 3 = 1)
''')

# Сохраняем изменения
connection.commit()

# Делаем выборку всех записей при помощи fetchall(), где возраст не равен 60 и выводим результат в консоль
cursor.execute('''
SELECT username, email, age, balance FROM Users WHERE age != 60
''')
records = cursor.fetchall()

# Выводим записи в нужном формате
for record in records:
    username, email, age, balance = record
    print(f"Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}")

# Закрываем соединение с базой данных
cursor.close()
connection.close()
