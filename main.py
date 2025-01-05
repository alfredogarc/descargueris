#iwr -useb https://christitus.com/win | iex
#pip install --upgrade python-for-android
#python.exe -m pip install --upgrade pip
#pip install --upgrade flet
#sdk update kotlin               esta no funciona
#flutter pub upgrade --major-versions
#flutter upgrade
#flet build apk --requirements=lzma
#https://www.youtube.com/watch?v=vHzTewRgLDQ&pp=ygUXY2FuY2lvbiBkZSBtYXVpIG1vYW5hIDI%3D
import os
#import instaloader
import yt_dlp
import flet as ft
#import shutil
import re

def main(page: ft.Page):
    page.title = "Descargador de Videos"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 500
    page.window_height = 600

    message = ft.Text()
    url_input = ft.TextField(label="Ingresa la URL del video", width=400)
    download_button = ft.ElevatedButton(text="Descargar")
    progress_bar = ft.ProgressBar(width=400, visible=False)
    videos = [
        ft.VideoMedia("")
    ]
    video_player = ft.Video(
        playlist=videos,
        width=400,
        height=300,
        autoplay=True,
        visible=True,
    )

    def progress_hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            if total > 0:
                progress = downloaded / total
                progress_bar.value = progress
                page.update()

    def download_youtube_video_yt_dlp(url):
        video = ""
        target_folder = 'videos'
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        ydl_opts = {
            #'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]',
            'format': 'bestvideo',
            'outtmpl': os.path.join(target_folder, 'youtube_%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                video = ydl.prepare_filename(info_dict)
            print(f"¡Descarga completada con éxito! Archivo: {video}")
        except Exception as e:
            print(f"Error al descargar el video de YouTube: {e}")
            video = ""
        
        return video

    #def download_instagram_video(post_url):
    #    video = ""
    #    try:
    #        L = instaloader.Instaloader(download_video_thumbnails=False, save_metadata=False, post_metadata_txt_pattern='')
    #        post = instaloader.Post.from_shortcode(L.context, post_url.split("/")[-2])
                
    #        target_folder = 'videos'
    #        if not os.path.exists(target_folder):
    #            os.makedirs(target_folder)

    #        def custom_progress(current, total):
    #            progress = current / total if total > 0 else 0
    #            progress_bar.value = progress
    #            page.update()

    #       L.download_post(post, target=target_folder, progress_callback=custom_progress)

    #        for file_name in os.listdir(target_folder):
    #            if file_name.endswith(('.mp4', '.jpg')):
    #                full_file_name = os.path.join(target_folder, file_name)
    #                if os.path.isfile(full_file_name):
    #                    extension = os.path.splitext(file_name)[1]
    #                    nombre_limpio = re.sub(r'[^a-zA-Z0-9_]', ' ', post.caption or "instagram_post")
    #                    nombre_limpio = nombre_limpio.strip().replace(' ', '_')
    #                    nuevo_nombre = f"instagram_{nombre_limpio}{extension}"
    #                    new_path = os.path.join(target_folder, nuevo_nombre)
    #                    os.rename(full_file_name, new_path)
    #                    video = new_path
    #                    break

    #    except Exception as e:
    #        print(f"Error al descargar el video de Instagram: {e}")
    #        video = ""

    #    return video

    def download_video(e):
        url = url_input.value
        video = ""
        message.value = "Descargando..."
        progress_bar.visible = True
        progress_bar.value = 0
        page.update()

        try:
            if "youtube.com" in url or "youtu.be/" in url:
                video = download_youtube_video_yt_dlp(url)
                message.value = "¡Video de YouTube descargado con éxito!"
            #elif "instagram.com" in url:
            #    video = download_instagram_video(url)
            #    message.value = "¡Video de Instagram descargado con éxito!"
            elif "tiktok.com" in url or "twitter.com" in url:
                message.value = "Descarga de TikTok y Twitter no implementada aún."
            else:
                message.value = "URL no válida. Por favor, ingresa una URL de YouTube o Instagram."
        except Exception as e:
            message.value = f"Error: {e}"

        progress_bar.visible = False

        if video:
            video_path = os.path.abspath(video)
            ver_video(video_path)
        else:
            ver_video("")

        page.update()

    def ver_video(archivo):
        video_path = archivo
        video_media = [ft.VideoMedia(video_path)]
       
        video = ft.Video(
            playlist = video_media,
            width=640,
            height=360,
            autoplay=True,
            visible=True,
        )
        container_video.content = video
        page.update()

    download_button.on_click = download_video

    container_video = ft.Container()
    page.add(
        ft.Column([
            url_input,
            download_button,
            progress_bar,
            message,
            container_video
        ]),
    )

if __name__ == "__main__":
    ft.app(target=main)
