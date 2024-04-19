import random
import flet as ft

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "TheEthicalVideo"
    page.window_always_on_top = True
    page.spacing = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_pause(e):
        for video in videos:
            video.pause()
        print("Video.pause()")

    def handle_play_or_pause(e):
        for video in videos:
            video.play_or_pause()
        print("Video.play_or_pause()")

    def handle_play(e):
        for video in videos:
            video.play()
        print("Video.play()")

    def handle_stop(e):
        for video in videos:
            video.stop()
        print("Video.stop()")

    def handle_next(e):
        for video in videos:
            video.next()
        print("Video.next()")

    def handle_previous(e):
        for video in videos:
            video.previous()
        print("Video.previous()")

    def handle_volume_change(e):
        for video in videos:
            video.volume = e.control.value
        page.update()
        print(f"Video.volume = {e.control.value}")

    def handle_playback_rate_change(e):
        for video in videos:
            video.playback_rate = e.control.value
        page.update()
        print(f"Video.playback_rate = {e.control.value}")

    def handle_seek(e):
        for video in videos:
            video.seek(10000)
        print(f"Video.seek(10000)")

    def handle_add_media(e):
        for video in videos:
            video.playlist_add(random.choice(sample_media))
        print(f"Video.playlist_add(random.choice(sample_media))")

    def handle_remove_media(e):
        r = random.randint(0, len(videos[0].playlist) - 1)
        for video in videos:
            video.playlist_remove(r)
        print(f"Popped Item at index: {r} (position {r+1})")

    def handle_jump(e):
        print(f"Video.jump_to(0)")
        for video in videos:
            video.jump_to(0)

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
            extras={
                "artist": "Thousand Foot Krutch",
                "album": "The End Is Where We Begin",
            },
            http_headers={
                "Foo": "Bar",
                "Accept": "*/*",
            },
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
        page.add(video)

    page.add(
        ft.Row(
            wrap=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.ElevatedButton("Play", on_click=handle_play),
                ft.ElevatedButton("Pause", on_click=handle_pause),
                ft.ElevatedButton("Play Or Pause", on_click=handle_play_or_pause),
                ft.ElevatedButton("Stop", on_click=handle_stop),
                ft.ElevatedButton("Next", on_click=handle_next),
                ft.ElevatedButton("Previous", on_click=handle_previous),
                ft.ElevatedButton("Seek s=10", on_click=handle_seek),
                ft.ElevatedButton("Jump to first Media", on_click=handle_jump),
                ft.ElevatedButton("Add Random Media", on_click=handle_add_media),
                ft.ElevatedButton("Remove Random Media", on_click=handle_remove_media),
            ],
        ),
        ft.Slider(
            min=0,
            value=100,
            max=100,
            label="Volume = {value}%",
            divisions=10,
            width=400,
            on_change=handle_volume_change,
        ),
        ft.Slider(
            min=1,
            value=1,
            max=3,
            label="PlaybackRate = {value}X",
            divisions=6,
            width=400,
            on_change=handle_playback_rate_change,
        ),
    )

ft.app(target=main)
