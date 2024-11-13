import os
#import pytube
import instaloader
from TikTokApi import TikTokApi
import yt_dlp
import flet as ft
#import nicegui as ng
import shutil  # Asegúrate de importar shutil
import re
#pip install instaloader TikTokApi yt_dlp
#git config --global --add safe.directory f:\SDks\tools\flutter\

message = ft.Text("")
video_player = ft.Video(width=400, height=300)  # Control de video

# Función para descargar videos de YouTube usando yt-dlp
def download_youtube_video_yt_dlp(url):
    video = ""
    target_folder = 'videos'
    carpeta_videos(target_folder)

    ydl_opts = {
        'format': 'best',  # Descargar la mejor calidad disponible
        #'outtmpl': '%(title)s.%(ext)s',  # Nombre del archivo de salida
        'outtmpl': 'videos/youtube_%(title)s.%(ext)s',  # Nombre del archivo de salida
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)  # No descargar, solo obtener información
            #formats = info_dict.get('formats', [])
            #for f in formats:
            #    print(f)
            #    print(f"ID: {f['format_id']}, Resolución: {f.get('height', 'N/A')}p, Tipo: {f['ext']}")
            ydl.download([url])

            video = ydl.outtmpl
        print("¡Descarga completada con éxito!")
    except Exception as e:
        print(f"Error al descargar el video de YouTube: {e}")
        video = ""
    
    return video

def carpeta_videos(target_folder):
    # Crear la carpeta videos si no existe
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

# Función para descargar videos de Instagram
def download_instagram_video(post_url):
    video = ""
    try:
        L = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(L.context, post_url.split("/")[-2])
        video_title = obtener_nombre_video_instagram(post.title)
        L.download_post(post, target=post.owner_username)

        source_folder = post.owner_username
        target_folder = 'videos'
        carpeta_videos(target_folder)

        # Copiar archivos
        for file_name in os.listdir(source_folder):
            if file_name.endswith('.txt') or file_name.endswith('.xz'):
                continue
            full_file_name = os.path.join(source_folder, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, target_folder)
                # Renombrar el archivo destino
                extension = os.path.splitext(file_name)[1]
                nombre_limpio = re.sub(r'[^a-zA-Z0-9_]', ' ', post.pcaption)
                nombre_limpio = nombre_limpio.rstrip('.')
                nuevo_nombre = f"instagram_{nombre_limpio}{extension}"
                os.rename(os.path.join(target_folder, file_name), os.path.join(target_folder, nuevo_nombre))
                video = f"{target_folder}/{nuevo_nombre}"

        # Eliminar la carpeta post.owner_username
        shutil.rmtree(source_folder)
      
    except Exception as e:
        print(f"Error al descargar el video de Instagram: {e}")
        video = ""

    return video


def download_tiktok_video(video_url):
    """Función para descargar un video de TikTok usando TikTokApi."""
    api = TikTokApi.get_instance()
    
    # Extraer el ID del video de la URL
    video_id = video_url.split('/')[-1].split('?')[0]
    
    try:
        # Obtener el video
        video = api.video(id=video_id)
        
        # Guardar el video en un archivo
        with open(f"{video_id}.mp4", 'wb') as f:
            f.write(video.bytes())
        
        print(f"Video de TikTok descargado: {video_id}.mp4")
    except Exception as e:
        print(f"Error al descargar el video de TikTok: {e}")

# Función para descargar videos de X (Twitter)
import yt_dlp

def download_x_video(video_url):
    """Función para descargar un video de la red social X usando yt-dlp."""
    ydl_opts = {
        'format': 'best',  # Descargar la mejor calidad disponible
        'outtmpl': '%(title)s.%(ext)s',  # Nombre del archivo de salida
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("¡Descarga completada con éxito!")
    except Exception as e:
        print(f"Hubo un error al descargar el video: {e}")

def obtener_nombre_video_instagram(nombre_archivo):
    inicio = nombre_archivo.find('[')
    fin = nombre_archivo.find(']')
    if inicio != -1 and fin != -1:
        return nombre_archivo[inicio + 1:fin]
    else:
        return None

   
def main(page: ft.Page):
    page.title = "Descargador de Videos"
    
    url_input = ft.TextField(label="Ingresa la URL del video", width=400)
    download_button = ft.ElevatedButton(text="Descargar", on_click=lambda e: download_video(url_input.value,page=page))
    
    #video_player = ft.Video(width=400, height=300, source="")  # Control de video
    page.add(url_input, download_button, message, video_player)

def download_video(url, page: ft.Page):
    print(f"url {url}")
    try:
        if "youtube.com" in url or "youtu.be/" in url:
            video = download_youtube_video_yt_dlp(url)
            message.value = "¡Video de YouTube descargado con éxito!"
        elif "instagram.com" in url:
            video = download_instagram_video(url)
            message.value = "¡Video de Instagram descargado con éxito!"
        elif "tiktok.com" in url:
            #download_tiktok_video(url)
            message.value = "No implementado aun"
            video_file = ""
            #message.value = "¡Video de TikTok descargado con éxito!"
        elif "twitter.com" in url:
            #download_x_video(url)
            message.value = "No implementado aun"
            video_file = ""
            #message.value = "¡Video de X descargado con éxito!"
        else:
            message.value = "URL no válida. Por favor, ingresa una URL de YouTube, Instagram, TikTok o X."
    except Exception as e:
        message.value = f"Error: {e}"
        return
    
    print(f"videos = {video}")
    
    ruta = os.path.dirname(os.path.abspath(__file__)) + "/"
    ruta = ruta + video
    ruta = ruta.replace('/', '\\')  # Reemplazar barras / por \
    video_player.source = video
    video_player.update()  # Actualizar el componente para mostrar el video
    page.update()


# Ejemplo de uso
if __name__ == "__main__":
    ft.app(target=main)


# Ejemplo de uso
#if __name__ == "__main__":
    # Reemplaza las URLs con las que deseas descargar
    #url = "https://www.youtube.com/watch?v=tR5XcSybxZA"
    #download_youtube_video_yt_dlp(url)
#    url = "https://www.tiktok.com/@usa_.86/video/7420590695481658630?is_from_webapp=1&sender_device=pc"
#    download_tiktok_video(url)
    #download_instagram_video("https://www.instagram.com/reel/DB9cnIQAl4V/?igsh=MTBmYzZqeWRjd2RpMA==")
    #url = "https://www.instagram.com/reel/DCImQrVvmpf/?utm_source=ig_web_copy_link"
    #url = "https://www.instagram.com/reel/DCIpZtctezW/?utm_source=ig_web_copy_link"
    #download_instagram_video(url)

    #download_tiktok_video("https://www.tiktok.com/@usuario/video/ejemplo")
    #download_x_video("https://twitter.com/usuario/status/ejemplo")