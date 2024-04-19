import flet as ft
from flet import *
from utils import *

class SettingsPage():
    def __init__(self, page: ft.Page):
        self.page = page
        self.content = ft.Column()

    def change_theme(self, e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        # Пример изменения темы (для демонстрации, реальная логика может отличаться)
        self.page.theme_mode = "dark" if self.page.theme_mode == "light" else "light"
        self.content.update()

    def configure_notifications(self, e):
        # Пример настройки уведомлений (заглушка для демонстрации)
        print("Настройка уведомлений...")

    def change_language(self, e, lang):
        # Пример смены языка интерфейса (заглушка для демонстрации)
        print(f"Выбран язык: {lang}")

    def exit_app(self, e):
        # Закрытие приложения или страницы
        self.page._close()

    def generate_buttons(self):
        # Создание кнопок для различных настроек
        theme_button = ft.TextButton(text="Сменить тему", on_click=self.change_theme)
        notifications_button = ft.TextButton(text="Настройки уведомлений", on_click=self.configure_notifications)
        
        # Выбор языка через выпадающий список
        language_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option("Русский"), ft.dropdown.Option("English")],
            on_change=self.change_language
        )
        
        exit_button = ft.TextButton(text="Выйти", on_click=self.exit_app)

        # Добавление элементов управления на страницу
        self.content.controls.extend([theme_button, notifications_button, language_dropdown, exit_button])

    def get_content(self):
        """Получение контента страницы."""
        self.generate_buttons()
        return self.content