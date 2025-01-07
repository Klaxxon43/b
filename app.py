import flet as ft, random
from flet import Page, MainAxisAlignment, TextField, TextAlign, Text
import sqlite3
import asyncio
from aiogram import Bot
import requests
import os, sys
import openai, httpx
# Ваш токен бота
BOT_TOKEN = '7665691978:AAE3M_XAYI4m6Qy7zorXrBCqrwg0MjsCelw'  # Замените на ваш токен бота
OPENAI_API_KEY = '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'
proxy= 'http://2NeYSVvR:dacqMbf7@172.120.50.179:63456'

client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY,
                            http_client=httpx.AsyncClient(
                                proxy=proxy,
                                transport=httpx.HTTPTransport(local_address="0.0.0.0")
                                ))

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
    gpt_input = TextField(text_align=TextAlign.CENTER, label='Введи свой вопрос')
    gpt_text = ft.Text('Пока что тут нечего нет. Введи свой запрос и тут появится ответ')
    user_memory = {}

    async def gpt(e):
        # Функция для получения ответа от OpenAI
            response = await client.chat.completions.create(
                messages=[{"role": "user",
                        "content": str(gpt_input)}],
                model = "gpt-4o-mini"
            )
            print(gpt_input.value)
            print(response.choices[0].message.content)
            gpt_text.value = response.choices[0].message.content

    async def auth(e):
        _login = login_input.value
        _pass = password_input.value
    
        user = check_user(_login, _pass)
        if user:
            page.clean()
            gptt = await gpt(gpt_input.value)
            # await send_message(user[0], 'Успешная авторизация!')
            next_content = ft.Container(
                ft.Row(
                    [
                        gpt_text,
                        gpt_input,
                        ft.ElevatedButton("Отправить", on_click=gpt),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=ft.padding.all(20),
            )
            page.add(next_content)
            page.update()

        else:
            page.add(Text("Неверный логин или пароль", text_align=TextAlign.CENTER))

    def mode(e):
        if page.theme_mode == 'dark':
            page.theme_mode = 'light'
        else: 
            page.theme_mode = 'dark'
        page.update()

    page.add(
        ft.Container(
            ft.Row(
                [
                ft.Column(                    
                    [ 
                        ft.Container(ft.Row(
                        [
                        Text("Авторизация", text_align=TextAlign.CENTER),
                        ft.IconButton(ft.icons.SUNNY, on_click=mode)
                        ], alignment=MainAxisAlignment.CENTER
                        ), padding=ft.padding.only(left=80)
                    ), 
                    login_input,
                    password_input,
                    ft.ElevatedButton("Авторизоваться", on_click=auth)
                    ]
            )], alignment = MainAxisAlignment.CENTER
                ), 
            )
        ),



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
        conn.execute("""
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
        conn.commit() #Не забываем подтверждать изменения
        conn.close()
        print("База данных инициализирована.")
    except sqlite3.OperationalError as e:
        print(f"Ошибка при создании базы данных: {e}")
    except Exception as e:
        print(f"Общая ошибка: {e}")





if __name__ == '__main__':
    init_db()
    ft.app(target=main) #, view=ft.AppView.WEB_BROWSER
    
