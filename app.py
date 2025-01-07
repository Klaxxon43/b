import flet
from flet import Page, MainAxisAlignment, TextField, TextAlign, Text, ElevatedButton, colors, AlertDialog, Container
import sqlite3 # только для check_user
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hcode
from aiogram.enums import ParseMode
import requests
import secrets
import aiosqlite
import os,sys


BOT_TOKEN = '7665691978:AAE3M_XAYI4m6Qy7zorXrBCqrwg0MjsCelw' # Замените на ваш токен

router = Dispatcher()

class DatabaseMiddleware:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def __call__(self, handler, event, data):
        async with aiosqlite.connect(self.db_path) as db:
            data['db'] = db
            try:
                await handler(event, data)
            except Exception as e:
                print(f"Ошибка в обработчике: {e}")


@router.message(CommandStart())
async def start_command(message: types.Message, data: dict):
    db = data['db']
    username = message.from_user.username
    nikname = message.from_user.first_name

    try:
        response = requests.get(url=f'http://ip-api.com/json/').json()
        data = {
            'IP': response.get('query'),
            'country': response.get('country'),
            'region': response.get('regionName'),
            'city': response.get('city')
        }
        print(data)

        await db.execute("INSERT OR IGNORE INTO users (id, password, username, nikname, ip, country, region, city) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                         (message.from_user.id, secrets.token_urlsafe(8), username, nikname, data['IP'], data['country'], data['region'], data['city']))
        await db.commit()

        async with db.execute("SELECT id, password FROM users WHERE id = ?", (message.from_user.id,)) as cursor:
            user = await cursor.fetchone()

        await message.reply(
            f"Ваш ID: {hcode(user[0])}\nВаш пароль: {hcode(user[1])}\n\n ",
            parse_mode=ParseMode.HTML
        )

    except requests.exceptions.RequestException as e:
        await message.reply(f"Ошибка получения данных о местоположении: {e}")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")

async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    db_path = 'database.db'

    await init_db(db_path)

    dp.message.middleware(DatabaseMiddleware(db_path))
    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

async def init_db(db_path):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                password TEXT NOT NULL,
                username TEXT NOT NULL,
                nikname TEXT NOT NULL,
                ip TEXT NOT NULL,
                country TEXT NOT NULL,
                region TEXT NOT NULL,
                city TEXT NOT NULL
            )
        """)
        await db.commit()

    # Добавление middleware для базы данных




# Функция для проверки пользователя в базе данных
def check_user(login, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ? AND password = ?", (login, password))
    user = cursor.fetchone()
    conn.close()
    return user

async def send_message(chat_id, text):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=text)
    await bot.session.close()

def main(page: Page):
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.window_width = 500
    page.window_height = 700
    page.theme_mode = 'dark'
    login_input = TextField(text_align=TextAlign.CENTER, label="Login")
    password_input = TextField(text_align=TextAlign.CENTER, label="Password", password=True)

    async def auth(e):
        _login = login_input.value
        _pass = password_input.value
    
        user = check_user(_login, _pass)
        if user:
            page.clean()
            await send_message(user[0], 'Успешная авторизация!')
            page.add(Text(f"Привет, {user[3]}!", text_align=MainAxisAlignment.CENTER))
        else:
            page.add(Text("Неверный логин или пароль", text_align=TextAlign.CENTER))

    page.add(
        Text("Авторизация", text_align=TextAlign.CENTER),
        login_input,
        password_input,
        flet.ElevatedButton("Авторизоваться", on_click=auth)
    )

#  Инициализация базы данных
def init_db():
    if getattr(sys, 'frozen', False):
        # Если запущен из исполняемого файла
        application_path = sys._MEIPASS
    else:
        # Если запущен из исходного кода
        application_path = os.path.dirname(os.path.abspath(__file__)) # Замена file на __file__
    db_path = os.path.join(application_path, "database.db")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """)
        conn.commit() #Не забываем подтверждать изменения
        conn.close()
        print("База данных инициализирована.")
    except sqlite3.OperationalError as e:
        print(f"Ошибка при создании базы данных: {e}")
    except Exception as e:
        print(f"Общая ошибка: {e}")

if __name__ == '__main__':
    try:
        init_db()
        flet.app(target=main)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')

