# Задача "Регистрация покупателей"

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import os

from crud_functions import get_all_products, initiate_db, add_user, is_included

# Создаем экземпляр бота с API-токеном и диспетчера
API_TOKEN = ''

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Инициализация базы данных
initiate_db()

# Получение всех продуктов с обработкой ошибок
try:
    all_products = get_all_products()
except Exception as e:
    print(f"Ошибка при получении продуктов: {e}")
    all_products = []

# Определение состояний для регистрации
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    growth = State()
    weight = State()

# # Определение состояний
# class UserState(StatesGroup):
#     age = State()
#     growth = State()
#     weight = State()


# Функция основного меню
@dp.message_handler(commands=['start'])
async def start_menu(message: types.Message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=create_main_keyboard())


# Создаем обычную клавиатуру
def create_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Выберите опцию")
    keyboard.row(KeyboardButton('Рассчитать'), KeyboardButton('Информация'))
    keyboard.add(KeyboardButton('Купить'))
    keyboard.add(KeyboardButton('Регистрация'))
    return keyboard

# Асинхронная функция обработки нажатия на кнопку "Регистрация"
@dp.message_handler(lambda message: message.text == "Регистрация")
async def sing_up(message: types.Message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

# Реализация логики обработки ввода имени пользователя, email и возраста
# Проверяем наличие пользователя с таким именем
# Если пользователь не существует, он добавляется в базу данных

# Функция, обернутая в message_handler, который реагирует на состояние RegistrationState.username
@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text

    # Если пользователь с таким message.text есть в таблице БД, то выводим "Пользователь существует, введите
    # другое имя" и запрашиваем новое состояние для RegistrationState.username.
    if is_included(username):
        await message.answer("Пользователь существует, введите другое имя")
        return

    # Если пользователя message.text ещё нет в таблице БД, то обновляются данные в состоянии username на message.text
    # Далее выводится сообщение "Введите свой email:" и принимается новое состояние RegistrationState.email.
    await state.update_data(username=username)
    await message.answer("Введите свой email:")
    await RegistrationState.email.set()

# Функция, обернутая в message_handler, который реагирует на состояние RegistrationState.email
@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    email = message.text

    # Обновляем данные в состоянии RegistrationState.email на message.text
    await state.update_data(email=email)

    # Выводим сообщение о вводе возраста
    await message.answer("Введите свой возраст:")

    # Ожидаем ввода возраста в атрибут RegistrationState.age
    await RegistrationState.age.set()

# Функция, обернутая в message_handler, который реагирует на состояние RegistrationState.age
@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    age = message.text

    # Обновляем данные в состоянии RegistrationState.age на message.text
    await state.update_data(age=age)

    # Берем все данные (username, email и age) из состояния
    user_data = await state.get_data()

    # и записываем в таблицу БД Users при помощи ранее написанной crud-функции add_user
    try:
        add_user(user_data['username'], user_data['email'], age)
        await message.answer("Регистрация прошла успешно")
    except Exception as e:
        await message.answer(f"Произошла ошибка при регистрации: {e}")

    # Завершаем прием состояний
    await state.finish()


# Создаем Inline меню для продуктов
def create_product_inline_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=4)
    for product in all_products:
        keyboard.insert(InlineKeyboardButton(product[1], callback_data=f"product_buying"))
    return keyboard


# Асинхронная функция обработки нажатия на кнопку 'Купить'
@dp.message_handler(lambda message: message.text == "Купить")
async def buy_handler(message: types.Message):
    await get_buying_list(message)


# Асинхронная функция обработки нажатия на кнопку 'Информация'
@dp.message_handler(lambda message: message.text == 'Информация')
async def main_menu_INFO(message: types.Message):
    await message.answer('Информация о боте...')


# Асинхронная функция обработки нажатия на кнопку 'Рассчитать'
@dp.message_handler(lambda message: message.text == 'Рассчитать')
async def main_menu_CALC(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=inline_menu())


# Создание Inline меню для расчёта калорий
def inline_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories'))
    keyboard.add(InlineKeyboardButton('Формулы расчёта', callback_data='formulas'))
    return keyboard


# Функция get_buying_list с обработкой ошибок при отправке фото
async def get_buying_list(message: types.Message):
    for product in all_products:
        product_info = f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}'
        await message.answer(product_info)

        # Попытка отправить изображение продукта
        try:
            # Предполагаем, что изображения называются product1.jpg и т.д.
            image_path = f'product{product[0]}.jpg'
            if os.path.exists(image_path):
                await message.answer_photo(photo=open(image_path, 'rb'))
            else:
                await message.answer("Изображение продукта отсутствует.")
        except Exception as e:
            await message.answer(f"Ошибка при отправке изображения: {e}")

    await message.answer("Выберите продукт для покупки:", reply_markup=create_product_inline_keyboard())


# Асинхронная функция обработки нажатия на кнопки продуктов
@dp.callback_query_handler(lambda call: call.data == "product_buying")
async def product_buying_handler(callback_query: types.CallbackQuery):
    await send_confirm_message(callback_query)


# Функция send_confirm_message
async def send_confirm_message(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Вы успешно приобрели продукт!")


# Асинхронная функция обработки нажатия на кнопку 'Формулы расчёта'
@dp.callback_query_handler(lambda call: call.data == 'formulas')
async def get_formulas(call: types.CallbackQuery):
    formula_message = "Формула Миффлина-Сан Жеора:\n" \
                      "Для мужчин: BMR = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) + 5\n" \
                      "Для женщин: BMR = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161"
    await call.message.answer(formula_message)


# Асинхронная функция обработки нажатия на кнопку 'Рассчитать норму калорий'. Показ двух кнопок с выбором пола
@dp.callback_query_handler(lambda call: call.data == 'calories')
async def choose_gender(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Для женщин', callback_data='female'))
    keyboard.add(InlineKeyboardButton('Для мужчин', callback_data='male'))
    await call.message.answer("Выберите пол:", reply_markup=keyboard)


# Асинхронная функция обработки выбора пола
@dp.callback_query_handler(lambda call: call.data in ['female', 'male'])
async def set_gender(call: types.CallbackQuery, state: FSMContext):
    # Сохраняем выбранный пол
    await state.update_data(gender=call.data)

    await call.message.answer("Введите свой возраст:")

    # Устанавливаем состояние age
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    # Получаем введенный возраст
    age = message.text

    # Сохраняем возраст в состоянии
    await state.update_data(age=age)

    # Запрашиваем рост
    await message.answer("Введите свой рост (в см):")

    # Переход к следующему состоянию
    await RegistrationState.growth.set()


# Функция для обработки ввода роста
@dp.message_handler(state=RegistrationState.growth)
async def set_growth(message: types.Message, state: FSMContext):
    # Получаем введенный рост
    growth = message.text

    # Сохраняем рост в состоянии
    await state.update_data(growth=growth)
    await message.answer("Введите свой вес (в кг):")

    # Переход к следующему состоянию
    await RegistrationState.weight.set()


# Функция для обработки ввода веса и расчета нормы калорий
@dp.message_handler(state=RegistrationState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    # Получаем введенный вес
    weight = message.text

    # Сохраняем вес в состоянии
    await state.update_data(weight=weight)

    # Получаем данные о пользователе
    user_data = await state.get_data()

    age = int(user_data['age'])
    gender = user_data['gender']
    growth = int(user_data.get('growth'))
    weight = int(user_data.get('weight'))

    # Производим расчет нормы калорий по формуле Миффлина-Сан Жеора в зависимости от выбора пола
    if gender == 'female':
        bmr = 10 * weight + 6.25 * growth - 5 * age - 161
        await message.answer(f"Ваша норма калорий (BMR): {bmr:.2f} ккал.")

    elif gender == 'male':
        bmr = 10 * weight + 6.25 * growth - 5 * age + 5
        await message.answer(f"Ваша норма калорий (BMR): {bmr:.2f} ккал.")

    # Завершаем, чтобы сохранить состояние
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
