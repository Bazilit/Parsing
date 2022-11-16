import requests
import os
import json
import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime


def selenium(url):
    options = webdriver.ChromeOptions()
    binary_yandex_driver_file = 'yandexdriver.exe'
    try:
        driver = webdriver.Chrome(binary_yandex_driver_file, options=options)
        driver.get(url=url)
        time.sleep(30)  # ставим паузу,чтобы успел прогрузиться весь контент.
        with open('casio/html_selenium.html', 'w', encoding="utf-8") as file:
            file.write(driver.page_source)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def collect_info():
    now_data = datetime.now().strftime("%d_%m_%Y")
    with open(f"casio/data_{now_data}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Артикул",
                "Брэнд",
                "Ссылка на продукт",
                "Ссылка на изображение"
            )
        )
    data = []
    with open("casio/html_selenium.html", encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    items_cards = soup.find_all("a", class_="product-item__link")
    for item in items_cards:
        product_articl = item.find("p", class_="product-item__articul").text.strip()
        product_url = "https://shop.casio.ru" + item["href"]
        product_brand = item.find("img", class_="product-item__brand-img")["alt"]
        url_img = "https://shop.casio.ru" + item.find("img", class_="product-item__img")["src"]
        data.append(
            {
             "Артикул": product_articl,
             "Брэнд": product_brand,
             "Ссылка на продукт": product_url,
             "Ссылка на изображение": url_img,

            }
        )
        with open(f"casio/data_{now_data}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    product_articl,
                    product_brand,
                    product_url,
                    url_img
                )
            )
    with open(f"casio/data_{now_data}.json", "a", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    url = "https://shop.casio.ru/catalog/"
    if not os.path.exists("casio"):
        os.mkdir("casio")
    selenium(url=url)
    collect_info()


if __name__ == '__main__':
    main()
