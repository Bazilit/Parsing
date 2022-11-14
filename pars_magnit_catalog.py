import requests
from bs4 import BeautifulSoup
import time
import random
import jpg2pdf
import os
import natsort

# ВАЖНО!
# Сам сайт магнита агрессивен к запросам и спокойно банит все подозрительное.
# Обязательно сохраняйте все html страницы и промежуточные файлы, на случай блокировки доступа к сайту.
# Работу по проверке запросов осуществляем только с локальных файлов.

# В случае подозрения DDOS атаки на сайт, IP адрес блокируется примерно на час.
# Ставьте длительные интервалы запросов для избежания блокировки.
# Заголовки обязательны!


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.5.710 Yowser/2.5 Safari/537.36",
    "accept": "*/*"
}
# Подгружаем страницу с каталогом. 
# В ней уже есть все ссылки на страницы каталогов.

url = 'https://magnit.ru/magazine/2022-10-31/5901241/#1'
req = requests.get(url, headers=headers)
src = req.text
with open('index.html', 'w', encoding="utf-8") as file:
    file.write(src)

# Считываем файл и собираем ссылки на картинки.
with open ('magnit/index.html', encoding="utf-8") as file:
    src = file.read()
soup = BeautifulSoup(src, "lxml")
imgs = soup.find_all("img", class_="journal__image")
link_list = []
for i in range(0,len(imgs)):
    link = 'https://magnit.ru' + imgs[i]['src']
    link_list.append(link)
with open('link_list.txt', 'a') as file:
    for line in link_list:
        file.write(f"{line}\n")

# Сохраняем изображения из полученных ранее ссылок.
with open("link_list.txt") as file:
    lines = [line.strip() for line in file.readlines()]
count = 0
for line in lines:
    r = requests.get(line, headers=headers)
    with open(f"magnit/{count}.jpg", "wb") as f:
        f.write(r.content)
    count += 1
    time.sleep(random.randrange(4, 8))

# Считываем картинки с директории с помощью os и сортируем их при помощи библиотеки natsort.
# Отсортированные данные передаем в цикл для создания pdf файла при помощи библиотеки jpg2pdf.
dir = os.listdir('magnit')
sort_dir = natsort.natsorted(dir,reverse=False)
with jpg2pdf.create('magnit.pdf') as pdf:
    for img in sort_dir:
        pdf.add(f'magnit/{img}')
