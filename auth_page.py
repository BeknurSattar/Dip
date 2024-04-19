import flet as ft
from utils import connect_db, hash_password

class AuthPage:
    def __init__(self, page: ft.Page, my_login_function, my_register_function):
        self.page = page
        self.my_login_function = my_login_function
        self.my_register_function = my_register_function
        self.generate_login_form()

    def login(self):
        username = self.username_entry.value.strip()  # Обрезаем пробелы
        password = self.password_entry.value
        hashed_password = hash_password(password)  # Хешируем пароль перед проверкой
        conn = connect_db()
        if conn is not None:
            try:
                cur = conn.cursor()
                cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, hashed_password))
                user = cur.fetchone()
                cur.close()
                if user:
                    print("Успешный вход.")
                    self.my_login_function()  # Переход на основное содержимое после успешного входа
                else:
                    self.page.update_alert(ft.Alert("Неверное имя пользователя или пароль.", open=True))
            except Exception as e:
                self.page.update_alert(ft.Alert(f"Ошибка при выполнении запроса: {e}", open=True))
            finally:
                conn.close()
        else:
            self.page.update_alert(ft.Alert("Не удалось подключиться к базе данных.", open=True))

    def toggle_password_visibility(self, e):
        self.password_entry.password = not self.show_password_checkbox.value
        self.page.update()

    def generate_login_form(self):
        # Создаем элементы формы
        title_text = ft.Text("Analiz", size=20, text_align="center", width=200)
        self.username_entry = ft.TextField(label="Имя пользователя", expand=True, width=200)
        self.password_entry = ft.TextField(label="Пароль", password=True, expand=True, width=200)
        self.show_password_checkbox = ft.Checkbox(label="Показать пароль")
        self.show_password_checkbox.on_change = self.toggle_password_visibility
        login_button = ft.TextButton(text="Вход", on_click=self.login)
        google_button = ft.ElevatedButton(text="Вход через Google", width=200, icon=ft.icons.G_MOBILEDATA)
        register_button = ft.TextButton(text="Регистрация", on_click=lambda e: self.my_register_function())

        login_form_content = ft.Column([
            title_text,
            self.username_entry,
            self.password_entry,
            self.show_password_checkbox,
            login_button,
            google_button,
            register_button
        ], spacing=10)

        login_form = ft.Container(
            content=login_form_content,
            padding=ft.margin.all(20),
            border_radius=ft.BorderRadius(top_left=20, top_right=20, bottom_left=20, bottom_right=20),
            width=550,
            bgcolor=ft.colors.RED,
        )

        self.page.add(login_form)
    
    def get_content(self):
        """Получение контента страницы."""
        return self.page
