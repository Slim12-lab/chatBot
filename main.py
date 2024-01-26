import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sql import print_list, insert_id, return_customer, insert_task, task_list, get_names, get_tgid, return_login

# Инициализация бота и диспетчера
API_TOKEN = '6713267020:AAH9blJA-GCE6t_w7y-JJZTkz01QBmwWi-o'
bot = Bot(API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
# Подключение к базе данных
conn = sqlite3.connect('slt3.db')
cursor = conn.cursor()

# Определение состояний для машины состояний
class AuthState(StatesGroup):
    waiting_for_login = State()
    waiting_for_password = State()
    waiting_for_task = State()
    waiting_for_perfomer = State()
    waiting_for_number = State()


kb = ReplyKeyboardMarkup(resize_keyboard=True,  
                         one_time_keyboard=True)

#для запуска
async def on_startup(_):
    print('Бот был успешно запущен!')
    await db_start()

#Обработка команды /cancel для прерывания состояний процесса
@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.message, state: FSMContext):
    if state is None:
        return
    
    await state.finish() 
    await message.reply("Вы прервали нынешний процесс.", reply_markup = kb)


# Обработчик команды /start
@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):

    # Отправляем приветственное сообщение с клавиатурой
    await message.answer(f"Вас приветствует бот-помощник! \n\n Чтобы приступить к работе, введите логин для авторизации в ответном сообщении.")

    # Устанавливаем состояние ожидания логина
    await AuthState.waiting_for_login.set()

# Обработчик ввода логина
@dp.message_handler(state=AuthState.waiting_for_login)
async def process_login(message: types.Message, state: FSMContext):
    # Получаем введенный логин
    async with state.proxy() as data:
        data['login'] = message.text
        print(data)

        await state.update_data(login=data['login'])
    # Проверяем наличие логина в базе данных
    cursor.execute("SELECT * FROM auth WHERE login=?", (data['login'],))
    user = cursor.fetchone()

    if user:
        # Логин найден, переходим к вводу пароля
        await state.update_data(login=data['login'])
        await message.answer(f"Логин найден✅ \n Введите пароль, чтобы завершить авторизацию в аккаунт.")
        await AuthState.waiting_for_password.set()
    else:
        # Логин не найден, просим ввести снова
        await message.answer(f"Логин не найден❌ \nПроверьте, не допущены ли ошибки. \n\nВведите верный логин в ответном сообщении.")

# Обработчик ввода пароля
@dp.message_handler(state=AuthState.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    password = message.text
    data = await state.get_data()

    # Проверяем логин и пароль в базе данных
    cursor.execute("SELECT * FROM auth WHERE login=? AND password=?", (data['login'], password))
    user = cursor.fetchone()

    if user:
        # Успешная авторизация
        # await message.answer("Вы успешно прошли авторизацию!")
        await insert_id(message.from_user.id, data['login'])

        # Отправляем сообщение с клавиатурой и устанавливаем состояние ожидания задачи
        button_task = KeyboardButton("/task")
        kb.add(button_task).insert(KeyboardButton("/list"))
        await message.answer(f"Авторизация пройдена успешно!\n\nВыберите действие, которое вас интересует:", reply_markup=kb)
        await state.finish()
    else:
        # Логин и пароль не совпадают, просим ввести снова
        await message.answer(f"Пароль не верный❌\nПроверьте, не допущены ли ошибки. \n\nВведите верный пароль в ответном сообщении.")


# Обработчик кнопки "Поставить задачу"
@dp.message_handler(commands=['task'])
async def process_task(message: types.Message, state: FSMContext):
    await AuthState.waiting_for_perfomer.set()
    # Пользователь нажал кнопку "Поставить задачу"
    await message.answer("Введите описание поручения:")

# Обработчик ввода описания задачи
@dp.message_handler(state=AuthState.waiting_for_perfomer, content_types=types.ContentType.TEXT)
async def process_task_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        data['login'] = await return_login(message.from_user.id)
        
    if data['login'] is None:
        # Обработка случая, когда не удалось получить логин
        await message.answer("Произошла ошибка. Пожалуйста, повторите попытку.")
        return    

    await message.answer('Выберите исполнителя по порядковому номеру:\n')
    await message.answer(await print_list(message.from_user.id))
        
    await AuthState.waiting_for_number.set()

# Обработчик ввода исполнителя
@dp.message_handler(state=AuthState.waiting_for_number, content_types=types.ContentType.TEXT)
async def process_task_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['perfomer_num'] = message.text
        print(data)

    async with state.proxy() as data:
        #вызов функции вставки задачи в базу данных
        await insert_task(data['login'], await return_customer(data['perfomer_num']), data['description'])
        await message.answer("Поручение успешно добавлена!", reply_markup=kb)
        await bot.send_message(await get_tgid(await return_customer(data['perfomer_num'])), f"У вас новая задача!\nОтправитель: {await get_names(data['login'])}\nОписание: {data['description']}")

    await state.finish()

# Обработчик команды /list
@dp.message_handler(commands=['list'], state='*')
async def help_command(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = await return_login(message.from_user.id)
        try:
            await message.answer(text="Вот список ваших поручений:")
            await message.answer(await task_list(data['login']), reply_markup=kb)
        except Exception as e:
            print(f"Ошибка при выполнении /list: {e}")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
