import requests
import os
import json
from datetime import datetime


def roscarservis_pars():
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.0.2419 Yowser/2.5 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    start_time = datetime.now()
    url = "https://roscarservis.ru/catalog/legkovye/?arCatalogFilter_458_1500340406=Y&set_filter=Y&sort%5Brecommendations%5D=asc&PAGEN_1=1"
    r = requests.get(url=url, headers=headers)
    page_count = r.json()["pagesCount"]
    data_list = []
    for page in range(1, page_count+1):
        url_pg = f"https://roscarservis.ru/catalog/legkovye/?arCatalogFilter_458_1500340406=Y&set_filter=Y&sort%5Brecommendations%5D=asc&PAGEN_1={page}"
        r = requests.get(url=url_pg, headers=headers)
        data = r.json()
        items_key = data["items"]
        stores = ["discountStores", "externalStores", "commonStores"]
        for item in items_key:
            total_amount = 0
            item_name = item["name"]
            item_price = item["price"]
            item_img = "https://roscarservis.ru" + item["imgSrc"]
            item_url = "https://roscarservis.ru" + item["url"]
            store_list = []
            for store in stores:
                if store in item:
                    if item[store] is None or len(item[store]) < 1:
                        continue
                    else:
                        for i in item[store]:
                            store_name = i["STORE_NAME"]
                            store_price = i["PRICE"]
                            store_amount = i["AMOUNT"]
                            total_amount += int(i["AMOUNT"])
                            store_list.append(
                                {
                                    "store_name": store_name,
                                    "store_price": store_price,
                                    "store_amount": store_amount,
                                }
                            )
            data_list.append(
                {
                    "name": item_name,
                    "price": item_price,
                    "img": item_img,
                    "url": item_url,
                    "stores": store_list,
                    "total_amount": total_amount,
                }
            )
        print(f"[Информация] Обработал {page} из {page_count}")
    time_now = datetime.now().strftime("%d_%m_%Y_%H_%M")
    with open(f"roscarservis/data_{time_now}.json", "a", encoding="utf-8") as file:
        json.dump(data_list, file, indent=4, ensure_ascii=False)
    dif_time = datetime.now() - start_time
    print(f"Затрачено времени {dif_time}")


def main():
    if not os.path.exists("roscarservis"):
        os.mkdir("roscarservis")
    roscarservis_pars()


if __name__ == "__main__":
    main()
