import requests
import os
import json
import subprocess
from dotenv import load_dotenv

# Загружаем токены из .env
load_dotenv()

# Твои данные
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
TWITCH_USERNAME = os.getenv("TWITCH_USERNAME")
OUTPUT_DIR = "downloads"

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
    return response.json()["data"][0]["id"]

# Получаем список видео
def get_latest_video(token, user_id):
    url = f"https://api.twitch.tv/helix/videos?user_id={user_id}&sort=time&type=archive&first=1"
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    videos = response.json().get("data", [])
    
    if not videos:
        return None

    return videos[0]["url"]  # Берем последнюю запись

# Скачиваем видео с помощью yt-dlp
def download_video(video_url):
    if not video_url:
        print("Нет доступных видео!")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    command = ["python", "-m", "yt_dlp", "-o", f"{OUTPUT_DIR}/%(title)s.%(ext)s", video_url]

    subprocess.run(command)

if __name__ == "__main__":
    token = get_twitch_token()
    user_id = get_user_id(token)
    video_url = get_latest_video(token, user_id)

    print(f"Последнее видео: {video_url}")

    download_video(video_url)
