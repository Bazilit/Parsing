import requests
from bs4 import BeautifulSoup
import json
import random
import time

# нижеприведенный код для получения ссылок на личные профили участников и создания файла с перечнем этих ссылок.

# person_url_list = []

# for i in range(0, 740, 20):
#     url = f"https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset={i}"
#     q = requests.get(url)
#     result = q.content
#     soup = BeautifulSoup(result, 'lxml')
#     persons = soup.find_all("a")

#     for person in persons:
#         person_url = person.get('href')
#         person_url_list.append(person_url)

# with open('person_url_list.txt', 'a') as file:
#     for line in person_url_list:
#         file.write(f"{line}\n")


# Основной код запроса

data_dict = []
count = 0

with open("person_url_list.txt") as file:
    lines = [line.strip() for line in file.readlines()]
    for line in lines:
        q = requests.get(line)
        result = q.content
        soup = BeautifulSoup(result, "lxml")
        person = soup.find(class_="bt-biografie-name").find("h3").text
        person_name_company = person.strip().split(',')
        person_name = person_name_company[0]
        person_company = person_name_company[1].strip()

        links = soup.find_all(class_="bt-link-extern")
        links_list = []
        for link in links:
            links_list.append(link.get('href'))

        data = {
            "person_name": person_name,
            "company_name": person_company,
            "social_networks": links_list
        }
        count += 1
        print(f"#{count}: {line} is done.")
        data_dict.append(data)

        with open("data.json", "w", encoding="utf-8") as json_file:
            json.dump(data_dict, json_file, indent=4, ensure_ascii=False)

        time.sleep(random.randrange(2, 3))
        # сайт блокирует частые запросы.Это обязательно, для исключения блокировки.
