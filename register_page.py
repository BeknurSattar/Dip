import flet as ft
import psycopg2
from psycopg2 import OperationalError, errors
from utils import *

def RegisterPage(page: ft.Page, on_success_register):
    # Функция подключения к базе данных


    def register():
        username = username_entry.value
        password = password_entry.value
        first_name = first_name_entry.value
        last_name = last_name_entry.value
        email = email_entry.value
        conn = connect_db()
        if conn is not None:
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO users (username, password, first_name, last_name, email) VALUES (%s, %s, %s, %s, %s)",
                            (username, password, first_name, last_name, email))
                conn.commit()
                cur.close()
                print("Регистрация успешна.")
                on_success_register()  # Переход на страницу входа или подтверждения
            except errors.UniqueViolation:
                print("Пользователь с таким именем уже существует.")
                conn.rollback()
            except Exception as e:
                print("Ошибка при регистрации: ", e)
            finally:
                conn.close()
        else:
            print("Не удалось подключиться к базе данных.")

    username_entry = ft.TextField(label="Имя пользователя", expand=True)
    password_entry = ft.TextField(label="Пароль", password=True, expand=True)
    first_name_entry = ft.TextField(label="Имя", expand=True)
    last_name_entry = ft.TextField(label="Фамилия", expand=True)
    email_entry = ft.TextField(label="Электронная почта", expand=True)

    register_button = ft.Button(text="Зарегистрироваться", on_click=lambda e: register())

    register_form = ft.Column(
        controls=[
            first_name_entry,
            last_name_entry,
            email_entry,
            username_entry,
            password_entry,
            register_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

    return register_form
