import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

VIDEO_DESCRIPTION = os.getenv("VIDEO_DESCRIPTION")
OUTPUT_DIR = "downloads"

# Настройка Selenium для Edge
options = webdriver.EdgeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Edge(options=options)
wait = WebDriverWait(driver, 20)  # Явное ожидание до 20 секунд

def wait_for_upload_to_finish():
    print("Ожидание завершения загрузки видео...")
    time.sleep(30)  # начальное ожидание для подстраховки
    while True:
        try:
            progress_element = driver.find_element(By.CSS_SELECTOR, "span.progress-label")
            text = progress_element.text
            print("Статус загрузки:", text)

            match = re.search(r"Осталось времени: (\d+) (секунд|минут)", text)
            if match:
                value = int(match.group(1))
                unit = match.group(2)
                seconds = value * 60 if unit == "минут" else value
                buffer = 10  # небольшой запас
                print(f"Ожидаем {seconds + buffer} секунд...")
                time.sleep(seconds + buffer)
                break
            elif "Обработка" in text or "Проверка" in text:
                print("Обработка... ждём ещё 10 секунд")
                time.sleep(10)
            else:
                print("Загрузка завершена или не определена. Продолжаем.")
                break
        except Exception as e:
            print("Не удалось найти индикатор загрузки, повторяем попытку...", e)
            time.sleep(5)

def upload_video(video_path):
    driver.get("https://www.youtube.com/upload")
    time.sleep(5)  # Ожидание загрузки страницы

    upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
    upload_input.send_keys(video_path)

    wait_for_upload_to_finish()

    # Ждём поле описания
    desc_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='description-container']//div[@id='textbox']")))
    desc_box.send_keys(VIDEO_DESCRIPTION)

    # Отмечаем "Нет, это видео не для детей"
    not_for_kids_radio = wait.until(EC.element_to_be_clickable((By.NAME, "VIDEO_MADE_FOR_KIDS_NOT_MFK")))
    not_for_kids_radio.click()

    # Нажимаем кнопки "Далее"
# Нажимаем кнопку "Далее" 3 раза
    for _ in range(3):
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//ytcp-button[@id='next-button']")))
        next_button.click()
        time.sleep(2)

    # Выбираем "Открытый доступ"
    public_radio = wait.until(EC.element_to_be_clickable((By.NAME, "PUBLIC")))
    public_radio.click()

    # Публикация
    publish_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//ytcp-button[@id='done-button']")))
    publish_button.click()

    time.sleep(5)  # Ожидание завершения загрузки
    print("Видео загружено!")

if __name__ == "__main__":
    input("Пожалуйста, войдите в YouTube вручную и нажмите Enter, когда будете готовы...")

    video_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(('.mp4', '.mkv', '.avi'))]
    if not video_files:
        print("Нет видео для загрузки.")
    else:
        latest_video = os.path.abspath(os.path.join(OUTPUT_DIR, video_files[-1]))
        upload_video(latest_video)

    driver.quit()
