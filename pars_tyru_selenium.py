import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# Ссылка на динамический сайт. Информация подгружается в виде api запросов с ответом, содержащим html страницу с данными.
url = 'https://tury.ru/hotel/most_luxe.php'

# подключаем selenium с драйвером на яндекс браузер.
# создаем программу, которая зафиксирует верстку и сохранит в виде html файла.
# Драйвер под версию браузера подгружаем отсюда(https://github.com/yandex/YandexDriver/releases)

def selenium(url):
    options = webdriver.ChromeOptions()
    binary_yandex_driver_file = 'yandexdriver.exe'
    try:
        driver = webdriver.Chrome(binary_yandex_driver_file, options=options)
        driver.get(url=url)
        time.sleep(15)  # ставим паузу,чтобы успел прогрузиться весь контент.
        with open('html_selenium.html', 'w', encoding="utf-8") as file:
            file.write(driver.page_source)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

# запускаем программу и после завершения открываем сохраненный html файл.
selenium(url)


with open('html_selenium.html', encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')
hotel_cards = soup.find_all('div', class_="hotel_card_dv")
hotel_url_list = []
for hotel_url in hotel_cards:
    hotel_url = 'https://tury.ru' + hotel_url.find('a').get('href')
    hotel_url_list.append(hotel_url)

with open('hotel_url_list.txt', 'a') as file:
    for line in hotel_url_list:
        file.write(f"{line}\n")
