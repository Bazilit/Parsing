import requests
from bs4 import BeautifulSoup
import lxml
import json
import re

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.5.710 Yowser/2.5 Safari/537.36'
}

url_list = []

for i in range(0, 120, 24):
    url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=&to_date=&where%5B%5D=2&where%5B%5D=3&where%5B%5D=4&maxprice=500&o={i}&bannertitle=May'
    req = requests.get(url=url, headers=headers)
    json_data = json.loads(req.text)
    html_response = json_data['html']
    with open(f'data_2/index_{i}.html', 'w', encoding="utf-8") as file:
        file.write(html_response)
    with open(f'data_2/index_{i}.html', encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    cards = soup.find_all('a', class_='card-details-link')
    for card in cards:
        card_url = 'https://www.skiddle.com' + card.get('href')
        url_list.append(card_url)

festival_result = []
# Чтобы не скучать во время работы парсера...
count = 0
for url in url_list:
    print(f'Итерация № {count}')
    print(url)
    req_url = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req_url.content, 'lxml')
    name_festival = soup.find("div", class_="MuiContainer-root MuiContainer-maxWidthFalse css-1krljt2").find("h1").text
    place = soup.select('div > span[style]')[1].text
    if soup.select('div > span[style]')[2].text == soup.select('div > span[style]')[0].text:
        price = 'No price information'
    else:
        price = soup.select('div > span[style]')[2].text
    if soup.select('div > span[style]')[0].text == 'TBC' or None:
        data = 'Еvent date not specified'
    else:
        data = soup.select('div > span[style]')[0].text
    if data == 'Еvent date not specified':
        month = soup.find("div", class_="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol").find('span').text.strip(', ').split()[0]
        year = soup.find("div", class_="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol").find('span').text.strip(', ').split()[1]
    else:
        month = soup.find("div", class_="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol").find('span').next_sibling.text.strip().split(', ')[0]
        year = soup.find("div", class_="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol").find('span').next_sibling.text.strip().split(', ')[1]
    festival_result.append(
        {
            'Year': year,
            'Month': month,
            'Data': data,
            'Festival_name': name_festival,
            'Festival_url': url,
            'Festival_place': place,
            'Price': price
        }
    )
    count += 1

with open('festival_result.json', 'a', encoding="utf-8") as file:
    json.dump(festival_result, file, indent=4, ensure_ascii=False)
