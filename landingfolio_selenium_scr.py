import time
import json
from selenium import webdriver
from bs4 import BeautifulSoup


# Изначальный сайт по запросу
# url = "https://www.landingfolio.com/"

# # Прокручиваем в ручную сайт до конца, чтобы подгрузились все страницы.
options = webdriver.ChromeOptions()
options.add_argument('log-level=3')
binary_yandex_driver_file = 'yandexdriver.exe'
driver = webdriver.Chrome(binary_yandex_driver_file, options=options)

# driver.get(url=url)
# time.sleep(100)

# with open('html_selenium_1.html', 'w', encoding="utf-8") as file:
#     file.write(driver.page_source)

with open('html_selenium.html', encoding="utf-8") as file:
    src = file.read()


def landingfolio(src):
    soup = BeautifulSoup(src, "lxml")
    data_url = soup.find_all("div", class_="overflow-hidden rounded-xl border border-gray-200")
    url_list = []
    for url in data_url:
        url_progect = "https://www.landingfolio.com" + url.find("a")["href"]
        url_list.append(url_progect)
    with open('url_list.txt', 'a') as file:
        for line in url_list:
            file.write(f"{line}\n")

    with open("url_list.txt") as file:
        lines = [line.strip() for line in file.readlines()]
    data = []
    for line in lines[0:100]:
        driver.get(url=line)
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        try:
            title = soup.find("h2", class_="text-2xl mb-2 font-bold text-gray-900 sm:text-3xl").text.strip()
        except:
            print(f"text error: {line}")
            title = "Нет названия"
            continue
        try:
            description = soup.find("p", class_="text-base font-normal leading-7 text-gray-600").text.strip()
        except:
            print(f"description error: {line}")
            description = "Нет описания"
            continue
        try:
            url = soup.find("div", class_="group flex items-center space-x-4 w-full").find("a")["href"]
        except:
            print(f"url error: {line}")
            url = "Нет ссылки на сайт"
            continue
        try:
            img = soup.find("div", class_="relative mt-8").find("img")["src"]
        except:
            print(f"img error: {line}")
            img = "Нет изображения"
            continue
        data.append(
                {
                 "Название проекта": title,
                 "Описание": description,
                 "Ссылка на сайт": url,
                 "Изображение": img,
                }
            )
    with open("data.json", "a", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    landingfolio(src)


if __name__ == "__main__":
    main()
