import requests
import json
import csv
import random
import time
from bs4 import BeautifulSoup

# url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.5.710 Yowser/2.5 Safari/537.36'
}

# req = requests.get(url, headers=headers)
# src = req.text

# with open ('caloria.html', 'w', encoding="utf-8") as file:
#     file.write(src)

# with open ('caloria.html', encoding="utf-8") as file:
#     src = file.read()

# soup = BeautifulSoup(src, 'lxml')

# all_products_hrefs = soup.find_all(class_='mzr-tc-group-item-href')
# all_categories_dict = {}
# for item in all_products_hrefs:
#     item_text = item.text
#     item_url = 'https://health-diet.ru' + item.get('href')
#     all_categories_dict[item_text] = item_url

# with open ('all_categories_dict.json', 'w', encoding="utf-8") as file:
#     # encoding="utf-8" - обязательно, для корректной кодеровки кириллицы.
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)
#     # ensure_ascii - чтобы не было проблем с кодировкой. Данная функция не экранирует символы.
#     # indent - это отступ в пробелах. Если его убрать, запись будет идти в строку.

with open('all_categories_dict.json', encoding="utf-8") as file:
    all_categories_dict = json.load(file)

iteration_count = int(len(all_categories_dict))-1
print(f"Всего итераций: {iteration_count}")
count = 0
for category_name, category_url in all_categories_dict.items():
    rep = [" ", "-", ", ", ",", "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")

    req = requests.get(url=category_url, headers=headers)
    src = req.text

    with open(f"data/{count}_{category_name}.html", "w", encoding="utf-8") as file:
        file.write(src)

    with open(f"data/{count}_{category_name}.html", encoding="utf-8") as file:
        file.read()

    soup = BeautifulSoup(src, "lxml")

    # проверка страницы на наличие таблицы с продуктами
    alert = soup.find(class_="uk-alert-danger")
    if alert is not None:
        continue

    # собираем заголовки таблицы
    table_head = soup.find(class_="uk-table mzr-tc-group-table uk-table-hover uk-table-striped uk-table-condensed").find("tr").find_all("th")
    products = table_head[0].text
    calorics = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    сarbohydrates = table_head[4].text

    with open(f"data/{count}_{category_name}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                products,
                calorics,
                proteins,
                fats,
                сarbohydrates
            )
        )

    # собираем данные о продуктах
    products_data = soup.find(class_="uk-table mzr-tc-group-table uk-table-hover uk-table-striped uk-table-condensed").find("tbody").find_all("tr")

    product_info = []

    for item in products_data:
        product_tds = item.find_all("td")
        title = product_tds[0].find("a").text
        calorics = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        сarbohydrates = product_tds[4].text
        product_info.append(
            {
                "Title": title,
                "Calorics": calorics,
                "Proteins": proteins,
                "Fats": fats,
                "Carbohydrates": сarbohydrates
            }
        )

        with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                 title,
                 calorics,
                 proteins,
                 fats,
                 сarbohydrates
                )
            )

    with open(f"data/{count}_{category_name}.json", "a", encoding="utf-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f"# Итерация {count}. {category_name} записан в файл csv...")
    iteration_count = iteration_count-1
    if iteration_count == 0:
        print("Работа завершена!")
        break

    print(f"Осталось {iteration_count} итераций...")
    time.sleep(random.randrange(2, 4))
