import requests
import os
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime


books_list = []


async def get_page_data(session, page):
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }
    url_pag = f"https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=cover&page={page}"
    async with session.get(url=url_pag, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, "lxml")
        books_in_page = soup.find_all("div", class_="genres-carousel__item")
        for book in books_in_page:
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
            books_list.append(
                {
                    "Название книги": book_title,
                    "Автор": book_author,
                    "Цена": book_price,
                    "Скидка": book_sale,
                    "Ссылка": url_book,
                    "Издательство": book_pubhouse,
                }
            )
        print(f"Обрабатываю {page} раздел...")

async def gather_data():
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }
    url = "https://www.labirint.ru/genres/2308/?available=1&paperbooks=1"

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), "lxml")
        pagination_numbers = int(soup.find("div", class_="pagination-numbers").find_all("a")[-1].text)
        tasks = []
        for page in range(1, pagination_numbers+1):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)
        await asyncio.gather(*tasks)


def main():
    start_time = datetime.now()
    if not os.path.exists("labirint"):
        os.mkdir("labirint")
    asyncio.get_event_loop().run_until_complete(gather_data())
    time_now = datetime.now().strftime("%d_%m_%Y_%H_%M")
    with open(f"labirint/data_{time_now}_async.json", "a", encoding="utf-8") as file:
        json.dump(books_list, file, indent=4, ensure_ascii=False)
    dif_time = datetime.now() - start_time
    print(f"Обработка завершена! Затрачено времени: {dif_time}.")


if __name__ == "__main__":
    main()
