import flet as ft
from flet import *
import cv2
from persondetection import DetectorAPI
import matplotlib.pyplot as plt
from fpdf import FPDF
import psycopg2
from datetime import datetime
from utils import *
import base64

# Словарь, сопоставляющий классы с идентификаторами камер


# Глобальная переменная для таймера
max_count3 = 0
framex3 = []
county3 = []
max3 = []
avg_acc3_list = []
max_avg_acc3_list = []
max_acc3 = 0
max_avg_acc3 = 0

class CamerasPage:

    def __init__(self, page: ft.Page):
        self.page = page
        self.content = ft.Column()
        self.pb = self.create_popup_menu_button()
        self.camera_ids = {
            1: 0,  # Камера для класса 1
            2: 'Videoes/unihub.mp4',
            3: '',
            4: ''  # Камера для класса 2
            # Добавьте больше классов и камер по мере необходимости
        }



        
    
    def open_cam(self, class_id):
        # global max_count3, framex3, county3, max3, avg_acc3_list, max_avg_acc3_list, max_acc3, max_avg_acc3
        # max_count3 = 0
        # framex3 = []
        # county3 = []
        # max3 = []
        # avg_acc3_list = []
        # max_avg_acc3_list = []
        # max_acc3 = 0
        # max_avg_acc3 = 0

        # Получаем идентификатор камеры для данного класса
        camera_id = self.camera_ids[class_id]

        # Настройка пути к файлу для сохранения на основе class_id
        # output_path = f'output_video_class_{class_id}.mp4'

        # writer = None
        # if output_path is not None:
        #     writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MJPG'), 10, (600, 600))

        # Теперь вызываем функцию detectByCamera без проверки args['output']
        self.detectByCamera(camera_id, class_id)



    def first_f(self, camera_id):
        first_frame = None 
        video = cv2.VideoCapture(camera_id)
        while True:
            frame = video.read()
            img = cv2.resize(frame, (800, 600))
            if first_frame is None:
                first_frame = img.copy()
        return first_frame

    # function defined to detect from camera
    def detectByCamera(self, camera_id, class_id):
        global max_count3, framex3, county3, max3, avg_acc3_list, max_avg_acc3_list, max_acc3, max_avg_acc3
        max_count3 = 0
        framex3 = []
        county3 = []
        max3 = []
        avg_acc3_list = []
        max_avg_acc3_list = []
        max_acc3 = 0
        max_avg_acc3 = 0

        # function defined to plot the people count in camera

        video = cv2.VideoCapture(camera_id)
        odapi = DetectorAPI()
        threshold = 0.7
        

        x3 = 0
        while True:
            check, frame = video.read()
            if not check:
                break
            img = cv2.resize(frame, (800, 600))

            boxes, scores, classes, num = odapi.processFrame(img)
            person = 0
            acc = 0
            for i in range(len(boxes)):
                if classes[i] == 1 and scores[i] > threshold:
                    box = boxes[i]
                    person += 1
                    cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), (255, 0, 0), 2)  # cv2.FILLED
                    cv2.putText(img, f'P{person, round(scores[i], 2)}', (box[1] - 30, box[0] - 8),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)  # (75,0,130),
                    acc += scores[i]
                    if (scores[i] > max_acc3):
                        max_acc3 = scores[i]

            if (person > max_count3):
                max_count3 = person



            # if writer is not None:
            #     writer.write(img)

            cv2.imshow("Analiz", img)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                # Функция остановки таймера
                stop_periodic_data_insert()
                break

            county3.append(person)
            x3 += 1
            framex3.append(x3)
            if (person >= 1):
                avg_acc3_list.append(acc / person)
                if ((acc / person) > max_avg_acc3):
                    max_avg_acc3 = (acc / person)
            else:
                avg_acc3_list.append(acc)

            start_periodic_data_insert(person, class_id)

        video.release()

        def cam_enumeration_plot():
            plt.figure(facecolor='orange', )
            ax = plt.axes()
            ax.set_facecolor("yellow")
            plt.plot(framex3, county3, label="Human Count", color="green", marker='o', markerfacecolor='blue')
            plt.plot(framex3, max3, label="Max. Human Count", linestyle='dashed', color='fuchsia')
            plt.xlabel('Time (sec)')
            plt.ylabel('Human Count')
            plt.legend()
            plt.title("Enumeration Plot")
            plt.show()

        def cam_accuracy_plot():
            plt.figure(facecolor='orange', )
            ax = plt.axes()
            ax.set_facecolor("yellow")
            plt.plot(framex3, avg_acc3_list, label="Avg. Accuracy", color="green", marker='o', markerfacecolor='blue')
            plt.plot(framex3, max_avg_acc3_list, label="Max. Avg. Accuracy", linestyle='dashed', color='fuchsia')
            plt.xlabel('Time (sec)')
            plt.ylabel('Avg. Accuracy')
            plt.title('Avg. Accuracy Plot')
            plt.legend()
            plt.show()

        def cam_gen_report():
            pdf = FPDF(orientation='P', unit='mm', format='A4')
            pdf.add_page()
            pdf.set_font("Arial", "", 20)
            pdf.set_text_color(128, 0, 0)
            pdf.image('Images/eyeee.png', x=0, y=0, w=210, h=297)

            pdf.text(125, 150, str(max_count3))
            pdf.text(105, 163, str(max_acc3))
            pdf.text(125, 175, str(max_avg_acc3))
            if (max_count3 > 25):
                pdf.text(26, 220, "Max. Human Detected is greater than MAX LIMIT.")
                pdf.text(70, 235, "Region is Crowded.")
            else:
                pdf.text(26, 220, "Max. Human Detected is in range of MAX LIMIT.")
                pdf.text(65, 235, "Region is not Crowded.")

            pdf.output('Crowd_Report.pdf')


        for i in range(len(framex3)):
            max3.append(max_count3)
            max_avg_acc3_list.append(max_avg_acc3)

        enumeration_button = TextButton(text="Enumeration\nPlot", on_click=lambda e: cam_enumeration_plot())
        self.content.controls.append(enumeration_button)

        avga_button = TextButton(text="Avg. Accuracy\nPlot", on_click=lambda e: cam_accuracy_plot())
        self.content.controls.append(avga_button)

        generate_button = TextButton(text="Generate  Crowd  Report", on_click=lambda e: cam_gen_report())
        self.content.controls.append(generate_button)

        back_button = TextButton(text="Back to menu", on_click=lambda e: self.back_to_menu())
        self.content.controls.append(back_button)

        self.content.update()

    def back_to_menu(self):
        """Возвращение в меню."""
        self.content.controls.clear()
        self.generate_buttons()
        self.content.update()


    def create_popup_menu_button(self):
        pb = ft.PopupMenuButton(
            content=ft.Text("Расположение камер"),
            items=[
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.icons.CHECK_BOX_OUTLINE_BLANK),
                            ft.Text("1x1"),
                        ]
                    ),
                    on_click=lambda _: self.change_button_layout(1),
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.icons.GRID_VIEW_ROUNDED),
                            ft.Text("2x2"),
                        ]
                    ),
                    on_click=lambda _: self.change_button_layout(2),
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.icons.GRID_3X3),
                            ft.Text("3x3"),
                        ]
                    ),
                    on_click=lambda _: self.change_button_layout(3),
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.icons.GRID_4X4),
                            ft.Text("4x4"),
                        ]
                    ),
                    on_click=lambda _: self.change_button_layout(4),
                ),
            ]
        )
        return pb



    sample_media = [
        ft.VideoMedia(
            "Videoes/unihub.mp4"
        ),
        ft.VideoMedia(
            "https://user-images.githubusercontent.com/28951144/229373718-86ce5e1d-d195-45d5-baa6-ef94041d0b90.mp4"
        ),
        ft.VideoMedia(
            "https://user-images.githubusercontent.com/28951144/229373716-76da0a4e-225a-44e4-9ee7-3e9006dbc3e3.mp4"
        ),
        ft.VideoMedia(
            "https://user-images.githubusercontent.com/28951144/229373695-22f88f13-d18f-4288-9bf1-c3e078d83722.mp4"
        ),
        ft.VideoMedia(
            "https://user-images.githubusercontent.com/28951144/229373709-603a7a89-2105-4e1b-a5a5-a6c3567c9a59.mp4",
        ),
    ]

    videos = []
    for i, media in enumerate(sample_media):  # Change the number to adjust how many videos you want to display
        video = ft.Video(
            expand=True,
            playlist=media,  # Adjust playlist slicing for each video
            playlist_mode=ft.PlaylistMode.LOOP,
            fill_color=ft.colors.BLUE_400,
            aspect_ratio=16/9,
            volume=100,
            autoplay=False,
            filter_quality=ft.FilterQuality.HIGH,
            muted=False,
            on_loaded=lambda e: print("Video loaded successfully!"),
            on_enter_fullscreen=lambda e: print("Video entered fullscreen!"),
            on_exit_fullscreen=lambda e: print("Video exited fullscreen!"),
        )
        videos.append(video)


    def open_video_in_new_window(self, index):
        self.content.controls.clear() 
        # self.page.update()
        videos = []
        for i, media in enumerate(self.sample_media):  # Change the number to adjust how many videos you want to display
            video = ft.Video(
                expand=True,
            playlist=media,  # Adjust playlist slicing for each video
            playlist_mode=ft.PlaylistMode.LOOP,
            fill_color=ft.colors.BLUE_400,
            aspect_ratio=16/9,
            volume=100,
            autoplay=False,
            filter_quality=ft.FilterQuality.HIGH,
            muted=False,
            on_loaded=lambda e: print("Video loaded successfully!"),
            on_enter_fullscreen=lambda e: print("Video entered fullscreen!"),
            on_exit_fullscreen=lambda e: print("Video exited fullscreen!"),
            )
            videos.append(video)
            self.content.controls.append(video)


    def open_dlg_modal(self):

        def close_dlg(e):
            dlg_modal.open = False
            self.page.update()

        actions = []
        for i, media in enumerate(self.videos):
            btn = ft.TextButton(f"Камера {i+1}", on_click=lambda _, index=media: self.open_video_in_new_window(index))
            actions.append(btn)
        actions.append(ft.TextButton("Отмена", on_click=close_dlg))  # Передаем ссылку на функцию без вызова

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Список доступных камер"),
            actions=actions,
            actions_alignment=ft.MainAxisAlignment.CENTER,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        self.page.dialog = dlg_modal
        dlg_modal.open = True
        self.page.update()




    

    def change_button_layout(self, layout):
        # Очищаем текущий контент страницы
        self.content.controls.clear()
        global box
        # Создаем разные расположения кнопок
        if layout == 1:
            self.content.controls.clear()
            for _ in range(1):
                row = ft.Row()
                for _ in range(1):
                    box = ft.Container(
                        content=ft.Column(
                            controls=[                     
                                ft.TextButton(content=ft.Text("Выбрать камеру"), on_click=lambda _: self.open_dlg_modal())                               
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        padding=5,
                        margin=5,
                        border_radius=5,
                        bgcolor=ft.colors.BLUE,
                        width=1360,
                        height=660,
                    )
                    row.controls.append(box)
                self.content.controls.append(row)
        
        elif layout == 2:
            self.content.controls.clear()
            for _ in range(2):
                row = ft.Row()
                for _ in range(2):
                    box = ft.Container(
                        content=ft.Column(
                            controls=[                          
                                ft.TextButton(content=ft.Text("Выбрать камеру"), on_click=lambda _: self.open_dlg_modal())                        
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        padding=5,
                        margin=5,
                        border_radius=5,
                        bgcolor=ft.colors.BLUE,
                        width=665,
                        height=320,
                    )
                    row.controls.append(box)
                self.content.controls.append(row)

        elif layout == 3:
            self.content.controls.clear()
            for _ in range(3):
                row = ft.Row()
                for _ in range(3):
                    box = ft.Container(
                        content=ft.Column(
                            controls=[                          
                                ft.TextButton(content=ft.Text("Выбрать камеру"), on_click=lambda _: self.open_dlg_modal())
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        padding=5,
                        margin=5,
                        border_radius=5,
                        bgcolor=ft.colors.BLUE,
                        width=440,
                        height=210,
                    )
                    row.controls.append(box)
                self.content.controls.append(row)  # Добавьте реализацию для 3x3

        elif layout == 4:
            self.content.controls.clear()
            for _ in range(4):
                row = ft.Row()
                for _ in range(4):
                    box = ft.Container(
                        content=ft.Column(
                            controls=[                            
                                ft.TextButton(content=ft.Text("Выбрать камеру"), on_click=lambda _: self.open_dlg_modal())                            
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        padding=5,
                        margin=5,
                        border_radius=5,
                        bgcolor=ft.colors.BLUE,
                        width=325,
                        height=150,
                    )
                    row.controls.append(box)
                self.content.controls.append(row)  # Добавьте реализацию для 4x4
        self.page.update()

    def boxx(self, box):
        box.content.controls.clear()
        box.content.controls.append(ft.Text("Камера выбрана"))
        self.page.update()



    def appbar(self):
        app_bar = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Мои камеры", style=ft.TextStyle(color=ft.colors.WHITE, weight="bold", size=20)),
                    self.pb
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            height=30,
        )
        return app_bar
    

    def get_content(self):

        app_bar = self.appbar()

        self.change_button_layout(1)
  
        main_layout = ft.Column(
        controls=[
            app_bar,
            self.content  # Включаем содержимое страницы (кнопки камер)
            ]
        )

        return main_layout