import requests
import os
import json
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime


# Первоначальная ссылка на интересующие книги.
url = "https://www.labirint.ru/genres/2308/?available=1&paperbooks=1"


def labirint(url):
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }
    r = requests.get(url=url, headers=headers)
    with open("labirint/index.html", "w", encoding="utf-8") as file:
        file.write(r.text)
    with open("labirint/index.html", encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    pagination_numbers = int(soup.find("div", class_="pagination-numbers").find_all("a")[-1].text)
    start_time = datetime.now()
    book_list = []
    for page in range(1, pagination_numbers + 1):
        print(f"Обрабатываю {page} раздел из {pagination_numbers}...")
        url_pag = f"https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=cover&page={page}"
        response = requests.get(url=url_pag, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        books_in_page = soup.find_all("div", class_="genres-carousel__item")
        for book in books_in_page: # try/except, тк временами данные в описание отсутствуют.
            try:
                url_book = "https://www.labirint.ru" + book.find("a", class_="product-title-link")["href"]
            except:
                url_book = "Ссылка на книгу отсутствует."
            
            try:
                book_author = book.find("a", class_="product-title-link")["title"].split(" - ")[0]
            except:
                book_author = "Автор книги не указан."
            
            try:
                book_title = book.find("a", class_="product-title-link")["title"].split(" - ")[1]
            except:
                book_title = "Название книги не указано."
            
            try:
                book_sale = book.find("span", class_="price-val")["title"]
            except:
                book_sale = "Скидка не указана."
            
            try:
                book_price = book.find("span", class_="price-val").find_all("span")[0].text + " ₽"
            except:
                book_price = "Цена не указана."
            
            try:
                book_pubhouse = book.find("a", class_="product-pubhouse__pubhouse")["title"]
            except:
                book_pubhouse = "Издательство не указано."
            
            book_list.append(
                {
                    "Название книги": book_title,
                    "Автор": book_author,
                    "Цена": book_price,
                    "Скидка": book_sale,
                    "Ссылка": url_book,
                    "Издательство": book_pubhouse,
                }
            )
        time.sleep(random.randrange(3, 6))
    dif_time = datetime.now() - start_time
    print(f"Обработка завершена! Затрачено времени: {dif_time}.")
    time_now = datetime.now().strftime("%d_%m_%Y_%H_%M")
    with open(f"labirint/data_{time_now}.json", "a", encoding="utf-8") as file:
        json.dump(book_list, file, indent=4, ensure_ascii=False)


def main():
    if not os.path.exists("labirint"):
        os.mkdir("labirint")
    labirint(url)


if __name__ == "__main__":
    main()
