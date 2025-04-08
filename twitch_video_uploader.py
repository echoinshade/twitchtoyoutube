import requests
import os
import json
import subprocess
from dotenv import load_dotenv

# Загружаем токены из .env
load_dotenv()

TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
TWITCH_USERNAME = os.getenv("TWITCH_USERNAME")  # Теперь никнейм берётся из .env
OUTPUT_DIR = "downloads"
VIDEO_INFO_FILE = "last_video.json"

# Получаем OAuth токен для Twitch API
def get_twitch_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params)
    return response.json().get("access_token")

# Получаем ID стримера
def get_user_id(token):
    url = f"https://api.twitch.tv/helix/users?login={TWITCH_USERNAME}"
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    data = response.json().get("data", [])
    return data[0]["id"] if data else None

# Получаем список видео (яркие моменты)
def get_videos(token, user_id):
    url = f"https://api.twitch.tv/helix/videos?user_id={user_id}&sort=time&type=highlight&first=50"
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.json().get("data", [])

# Выбор видео
def select_video(videos):
    if not videos:
        print("❌ Нет доступных видео!")
        exit()
    
    for idx, video in enumerate(videos):
        print(f"{idx + 1}. {video['title']} ({video['created_at']})")
    
    while True:
        try:
            choice = int(input("Выберите видео для загрузки (номер): ")) - 1
            if 0 <= choice < len(videos):
                return videos[choice]["url"], videos[choice]["created_at"], videos[choice]["title"]
            else:
                print("❌ Некорректный номер. Попробуйте снова.")
        except ValueError:
            print("❌ Введите числовой номер из списка.")

# Скачивание видео
def download_video(video_url, title):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    output_path = f"{OUTPUT_DIR}/{title}.mp4"
    command = ["python", "-m", "yt_dlp", "-o", output_path, video_url]
    subprocess.run(command)
    
    return output_path

# Сохранение данных для Boosty
def save_video_info(video_path, video_date):
    with open(VIDEO_INFO_FILE, "w", encoding="utf-8") as f:
        json.dump({"video_path": video_path, "video_date": video_date}, f)
    print(f"✅ Данные сохранены в {VIDEO_INFO_FILE}")

if __name__ == "__main__":
    token = get_twitch_token()
    user_id = get_user_id(token)
    
    if not user_id:
        print(f"❌ Не удалось получить user_id для {TWITCH_USERNAME}. Проверьте данные!")
        exit()

    videos = get_videos(token, user_id)
    video_url, video_date, video_title = select_video(videos)
    video_path = download_video(video_url, video_title)
    save_video_info(video_path, video_date)

    print(f"✅ Видео скачано с канала {TWITCH_USERNAME}. Теперь запустите `boosty_uploader.py` для загрузки!")
