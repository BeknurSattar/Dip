import flet as ft
from flet import *
import psycopg2
from datetime import datetime
from utils import *

class DataPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.content = ft.Column()


    def fetch_and_display_data(self, class_id):
        """Получение и отображение данных."""
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT detection_date, people_count FROM occupancy WHERE class_id = %s ORDER BY detection_date DESC LIMIT 10;", (class_id,))
        rows = cur.fetchall()
        display_text = f"Last 10 detections for class {class_id}:\n\n"
        for row in rows:
            display_text += f"Date: {row[0]}, Count: {row[1]}\n"
        self.data_label.value = display_text
        cur.close()
        conn.close()
        self.content.update()

    def show_class_data(self, class_id):
        """Отображение данных класса."""
        self.content.controls.clear()
        self.data_label = Text(value="Data will be shown here")
        self.content.controls.append(self.data_label)

        fetch_data_button = TextButton(text="Fetch Data", on_click=lambda e: self.fetch_and_display_data(class_id))
        self.content.controls.append(fetch_data_button)

        back_button = TextButton(text="Back to menu", on_click=lambda e: self.back_to_menu())
        self.content.controls.append(back_button)

        self.content.update()

    def back_to_menu(self):
        """Возвращение в меню."""
        self.content.controls.clear()
        self.generate_buttons()
        self.content.update()


    def create_button(self, index):
        """Создание кнопки для аудитории."""
        return TextButton(
            content=Text(f"Данные аудиторий {index}"),
            on_click=lambda e, i=index: self.show_class_data(i)
        )


    def generate_buttons(self):
        """Генерация кнопок для аудиторий."""
        self.content.controls.clear()  # Очищаем текущий контент
        for i in range(1, 11):
            self.content.controls.append(self.create_button(i))

    def get_content(self):
        """Получение контента страницы."""
        self.generate_buttons()
        return self.content
