from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from module_14.homework_14_5.crud_functions import *

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard = True)
button = KeyboardButton(text = 'Рассчитать')
button_2 = KeyboardButton(text = 'Информация')
button_3 = KeyboardButton(text = 'Купить')
button_4 = KeyboardButton(text = 'Регистрация')
kb.row(button, button_2, button_3, button_4)

inline_kb = InlineKeyboardMarkup(resize_keyboard = True)
inline_button = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data = 'calories')
inline_button_2 = InlineKeyboardButton(text = 'Формулы расчёта', callback_data = 'formulas')
inline_kb.row(inline_button, inline_button_2)

buy_menu = InlineKeyboardMarkup(resize_keyboard = True)
buy_menu_button_1 = InlineKeyboardButton(text = 'Product1', callback_data='product_buying')
buy_menu_button_2 = InlineKeyboardButton(text = 'Product2', callback_data='product_buying')
buy_menu_button_3 = InlineKeyboardButton(text = 'Product3', callback_data='product_buying')
buy_menu_button_4 = InlineKeyboardButton(text = 'Product4', callback_data='product_buying')
buy_menu.row(buy_menu_button_1, buy_menu_button_2, buy_menu_button_3, buy_menu_button_4)

initiate_db()
products = get_all_products()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler(text = ['Рассчитать'])
async def sing_up(message):
    await message.answer('Выберите опцию:', reply_markup = inline_kb)

@dp.message_handler(text = ['Регистрация'])
async def main_menu(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    username = message.text
    if is_included(username):
        await message.answer('Пользователь существует, введите другое имя')
        return

    await state.update_data(username=message.text)
    await message.answer('Введите свой email:')
    await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age = message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer('Вы успешно зарегистрированы!')
    await state.finish()

@dp.message_handler(text = ['Купить'])
async def get_buying_list(message):
    for product in products:
        id_, title, description, price = product
        await message.answer(f'Название: {title} | Описание: {description} | Цена: {price}')
        with open(f'path/to/file/Product{id_}.png', 'rb') as img:
            await message.answer_photo(img)
    await  message.answer('Выберите продукт для покупки: ', reply_markup=buy_menu)

@dp.callback_query_handler(text = ['formulas'])
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.callback_query_handler(text = ['calories'])
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.callback_query_handler(text = ['product_buying'])
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    result = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await message.answer(f'Ваша норма калорий {result:.2f}')
    await state.finish()

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)