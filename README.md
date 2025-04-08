# Гайд по работе с twitch_downloader.py и youtube_uploader.py

## 📌 Описание программ
Этот проект позволяет **автоматически скачивать видео с Twitch и загружать их на Youtube**

**twitch_downloader.py** – скачивает видео с Twitch (только последний опубликованный).

**twitch_video_downloader.py** – скачивает видео с Twitch (только яркие моменты(хайлайты)).

**youtube_uploader.py** – загружает скачанное видео на Youtube.

## 🔧 1. Подготовка к работе
Установим необходимые зависимости

Открываем командную строку (cmd) и вводим:

`pip install requests selenium python-dotenv yt-dlp`

( Если у тебя Windows 7/8 и yt-dlp не работает, попробуй:
`pip install yt-dlp --no-deps`)

## Настройка Twitch API

Найди файл .env (в папке).

Впиши туда:

TWITCH_USERNAME=**твой_ник_на_твиче**

TWITCH_CLIENT_ID=**твой_client_id**

TWITCH_CLIENT_SECRET=**твой_client_secret**

VIDEO_DESCRIPTION=**описание_к_видео**

### Как получить client_id и client_secret:

1) Зарегистрируйся на [Twitch console.](https://dev.twitch.tv/console)
2) Выбери Заявки
3) Введи любое название (лучше осмысленное!)
4) В OAuth Redirect URL указать https://localhost
5) Категория Application Integraion
6) Получам client_id и client_secret

## 📥 2. Скачивание видео с Twitch

Запустим **twitch_downloader.py**

Введём в командной строке:

`python twitch_downloader.py`

Программа начнет скачивание последнего опубликованного стрима

**ИЛИ**

Запустим **twitch_video_downloader.py**

Введём в командной строке:

`python twitch_video_downloader.py`

Программа покажет список хайлайтов, доступных к скачиванию.

✅ Видео будет скачано в папку downloads/ при проекте

## 📤 3. Загрузка видео на Youtube

### 1. Открой браузер Edge в режиме отладки

Закрой все окна Edge, затем запусти его командой в командной строке:

`"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium"`

(если у тебя 64-битная версия, путь может быть `C:\Program Files\Microsoft\Edge\Application\msedge.exe`).

### 2. Перейди на Youtube и залогинься

Открой вручную https://www.youtube.com/ и убедись, что ты авторизован.

### 3. Запусти youtube_uploader.py

Напиши в командной строке:

`python youtube_uploader.py`

✅ Скрипт откроет старницу загрузки Youtube, вставит заголовок, описание, прожмет все кнопки и опубликует по готовности

🔄 Повторная загрузка видео

Чтобы загрузить ещё одно видео:

Снова запусти **twitch_downloader.py**.

Затем снова **youtube_uploader.py**.

Скрипт выгружает последнее загруженное видео! 

# ❓ Возможные ошибки и их решения

## 1. Edge не запускается с отладкой

Ошибка:

"msedge.exe" не является внутренней или внешней командой

Решение:

Используй полный путь:

`"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium"`

Если Edge не установлен, скачай его здесь.

## 2. Ошибка при скачивании видео

Ошибка:

yt-dlp: command not found

Решение:

Переустанови yt-dlp:

`pip install yt-dlp --upgrade`

Если не помогает, скачай yt-dlp.exe и добавь его в папку со скриптом.

## 3. Ошибка "не найдено видео"

Ошибка:

❌ Нет доступных видео!

Решение:

Проверь, есть ли у тебя яркие моменты (Highlights) на Twitch.

Попробуй изменить `type=highlight` на `type=all` в get_videos() в **twitch_video_downloader.py**.

## 4. Ошибка при открытии страницы загрузки ютуба

Например, вы хотели запустить youtube_uploader.py во второй раз. Он не работает.

Вы:

1. Запускаете youtube_uploader.py
2. Прожимаете ДВАЖДЫ ctrl+c
3. Обновляете страницу ютуба
4. Запускаете youtube_uploader.py еще раз

Должно помочь!

## Мой пример работы с консолью

`E:

cd E:\downloader

python twitch_downloader.py

"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium_edge"

python youtube_uploader.py`
