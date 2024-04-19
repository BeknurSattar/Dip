import flet as ft
from flet import *
from data_page import DataPage
from cameras_page import CamerasPage
from settings_page import SettingsPage
from home_page import home_page
from auth_page import AuthPage
import threading
from utils import *
import base64


def main(page: ft.Page):
    page.full_screen = True

    is_authenticated = False  # Статус авторизации пользователя

    def my_login_function():
        nonlocal is_authenticated
        is_authenticated = True
        update_body_content() 

    def my_register_function():
        # Переключение на страницу регистрации
        registration_page = RegisterPage(page, on_success_register=lambda: AuthPage(page, my_login_function, my_register_function))
        page.controls.clear()
        page.controls.append(registration_page)
        page.update()



    def on_exit_click(e):
        print("Выход")

    def update_body_content():
        # nonlocal selected_index
        # page.controls.clear()
        # if not is_authenticated:
        #     # Отображаем страницу авторизации
        #     page.controls.append(AuthPage(Page, my_login_function, my_register_function).get_content()) 
        # else:
            if selected_index == 0:
                body_content.controls = home_page()
            elif selected_index == 1:
                body_content.controls.clear()
                body_content.controls.append(DataPage(page).get_content())
            elif selected_index == 2:
                body_content.controls.clear()
                body_content.controls.append(CamerasPage(page).get_content())
            elif selected_index == 3:
                body_content.controls.clear()
                body_content.controls.append(SettingsPage(page).get_content())
            else:
                body_content.controls = [ft.Text("Неизвестная страница")]
            body_content.update()

    def on_navigation_selected(e):
        nonlocal selected_index
        selected_index = rail.selected_index
        update_body_content()
        page.update() 

    selected_index = 0  # Инициализируем с начальным индексом навигации

    app_bar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("AnaLiz", style=ft.TextStyle(color=ft.colors.WHITE, weight="bold", size=20)),
                ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE, selected_icon=ft.icons.ACCOUNT_CIRCLE, on_click=lambda e: print("Профиль")),
                ft.IconButton(icon=ft.icons.EXIT_TO_APP, selected_icon=ft.icons.EXIT_TO_APP, on_click=on_exit_click),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        height=56,
    )

    rail = ft.NavigationRail(
        selected_index=selected_index,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.HOME, label="Главная страница"),
            ft.NavigationRailDestination(icon=ft.icons.STORAGE, label="Данные"),
            ft.NavigationRailDestination(icon=ft.icons.CAMERA_ALT, label="Камеры"),
            ft.NavigationRailDestination(icon=ft.icons.SETTINGS, label="Настройки"),
        ],
        on_change=on_navigation_selected,
    )

    body_content = ft.Column(
        controls=[],
        alignment=ft.MainAxisAlignment.START,
        expand=True
    )

    page_layout = ft.Row(
        controls=[
            rail,
            ft.VerticalDivider(width=1),
            body_content
        ],
        expand=True
    )

    page.add(ft.Column(controls=[app_bar, page_layout], expand=True))
    update_body_content()  # Первоначальное обновление содержимого

ft.app(target=main)
