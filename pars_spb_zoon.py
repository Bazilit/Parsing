import requests
import time
import re
import random
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


url = 'https://spb.zoon.ru/medical/'

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.0.2419 Yowser/2.5 Safari/537.36"
}

def get_sourc_html(url):
    options = webdriver.ChromeOptions()
    binary_yandex_driver_file = "yandexdriver.exe"
    driver = webdriver.Chrome(binary_yandex_driver_file, options=options)
    driver.maximize_window()
    try:
        driver.get(url=url)
        time.sleep(10)

        while True:
            find_more_elements = driver.find_element(By.CLASS_NAME, "catalog-button-showMore")
            if driver.find_elements(By.CLASS_NAME, "button-show-more"):
                with open("spb/spb_index.html", "w", encoding="utf-8") as file:
                    file.write(driver.page_source)
                break
            else:
                actions = ActionChains(driver)
                actions.move_to_element(find_more_elements).perform()
                time.sleep(10)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def get_items_url(file_patch):
    with open(file_patch, encoding="utf-8") as file:
        src = file.read()
    url_list = []
    soup = BeautifulSoup(src, "lxml")
    data_urls = soup.find_all("h2", class_="minicard-item__title")
    for data in data_urls:
        url = data.find("a")["href"]
        url_list.append(url)
    with open(r"spb\url_list.txt", "w", encoding="utf-8") as file:
        for url in url_list:
            file.write(f"{url}\n")
    return(print("[Информация] Обработка url ссылок завершена!"))


def get_data(file_patch):
    with open(file_patch, encoding="utf-8") as file:
        url_list = file.readlines()
        clear_url = [url.strip() for url in url_list]
    result_list = []
    count = 0
    len_url = len(url_list)
    for url in clear_url:
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        try:
            title = soup.find("h1", class_="service-page-header--text z-text--montserrat m0").find("span").text.strip()
        except:
            title = None
        phone_list = []
        try:
            phones = soup.find("div", class_="service-phones-list").find_all("a", class_="tel-phone js-phone-number")
            for phone in phones:
                item_phone = phone["href"].split(":")[-1].strip()
                phone_list.append(item_phone)
        except:
            phone_list = None
        try:
            address = soup.find("address", class_="iblock").text.strip()
        except:
            address = None
        try:
            main_network = soup.find(text=re.compile("Сайт|Официальный сайт|Компания в сети")).find_next().text.strip()
        except:
            main_network = None
        result_list.append(
            {
                "Имя": title,
                "Адрес": address,
                "Телефоны": phone_list,
                "Сайт": main_network,
            }
        )
        time.sleep(random.randrange(1, 3))
        if count % 10 == 0:
            time.sleep(random.randrange(1, 3))
        print(f"[Информация]: Обрабатываю {count}/{len_url} ...")
        count += 1
    with open("spb/result.json", "w", encoding="utf-8") as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)
    return "[+] Сбор информации завершен успешно!"


def main():
    get_sourc_html(url)
    get_items_url(file_patch="spb\spb_index.html")
    get_data(file_patch=r"spb\url_list.txt")


if __name__ == "__main__":
    main()
