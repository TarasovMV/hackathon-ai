from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor
import csv

# URL для GET-запроса
menu_url = 'https://twork.tinkoff.ru/knowledge-base/api/sections/list?spaceCode=kwb_default_space'
sections_url = 'https://twork.tinkoff.ru/knowledge-base/api/subsections'
article_url = 'https://twork.tinkoff.ru/knowledge-base/api/articles'
# Куки в виде строки
cookie_str = 'Pwuid=1a322b8faf9f4510a1532f994f7d71e1; stDeIdU=1a322b8faf9f4510a1532f994f7d71e1; sso_used=true; idsrv.uid=9c5d1ce1-3923-4790-9a06-6d44a97ba920; dsp_click_id=no%20dsp_click_id; _ym_uid=1723619321745406654; _ym_d=1723619321; dco.id=7399f3e2-06fb-4052-a8a7-0000115cb11e; userType=Visitor; amp_5a7f16=7a-sIB-4rFLI0c3IUJYECM...1i5s8ve1g.1i5s8ve1g.0.0.0; _ga=GA1.2.464451416.1723791511; _ga_EB19KZQJXZ=GS1.1.1724304570.4.1.1724304812.60.0.0; _ga_43H68Z69W3=GS1.1.1724304570.4.1.1724304812.60.0.0; utm_source=search; utm_date_set=1727684684986; Pwuid_last_update_time=1729232837793; Pwuid_visit_id=v1%3A0000125%3A1729266715883%3A1a322b8faf9f4510a1532f994f7d71e1; idsrv.login-id=vF0vS3DBkCn9oTgf7NLi; idsrv.time=1729355634; idsrv=CfDJ8CQxqrVrNhRIoA_pG3fqKDyU7lpCVGDQy1v9AK8fCInyX_ECwJp7J2GBbzmTuSNRJYyxSyPmc2Jr2rAWCR_ovNJnkU2diUYNYXeqkP1eGJoqmbN5OhnVG0ypjFmiTMjuOCIRp_l6M_azEVhuodR5sg3Kecxk7tfC7IU9NW6Sc2sIlPx4xz04Bcl1xSIin5asOi5uNaywWbwKVGre5DHvIUVibTJXk7jyAh888DE45ESdoPywbRYR7bKv45UOXYSmxtvWsQEB4442VA4vHCckN3w; _twork_oauth2_proxy=djIuWDNSM2IzSnJYMjloZFhSb01sOXdjbTk0ZVMwMVltTXpZekJtT0RoaFpEWm1aalptWkRWaU5HSTVZakJtTmpkaFpETXdNUS56eVhFckZKT2g3TzMyczNLYU0zaldR|1729355634|O80BBXyjgHiD7XZuf5ixHh7fVbrRj6zRFAIDrOm3gX0=; vIdUid=19dcccf9-9ee6-4227-9789-84531bacfda7; stSeStTi=1729355635274; stLaEvTi=1729355764493'
# Элементы меню
valid_menu_items = ['SME. Онлайн-бухгалтерия', 'SME. Бухгалтерское обслуживание']
# Заголовки, в которые передаем cookie
headers = {'Cookie': cookie_str}

def get_request(url):
    # Выполнение запроса с заголовком, содержащим куки
    response = requests.get(url, headers=headers, verify=False)

    # Проверка статуса ответа
    if response.status_code == 200:
        result = response.json()
    else:
        raise Exception(f'Ошибка: {response.status_code}')

    return result


menu = get_request(menu_url)

menu_id_items = []
for item in menu[3]['subsections']:
    if item['name'] in valid_menu_items:
        menu_id_items.append(item['id'])

print(menu_id_items)

article_id_items = []

for menu_id in menu_id_items:
    data = get_request(f'{sections_url}/{menu_id}')
    for node in data.get("categoryNodes", []):
        for child in node.get("children", []):
            article = child.get("article")
            if article and "id" in article:
                article_id_items.append(article["id"])

print(article_id_items)

knowledge_items = []
article_urls = list(map(lambda article_id: f'{article_url}/{article_id}', article_id_items))

with ThreadPoolExecutor() as executor:
    article_responses = executor.map(get_request, article_urls)

for data in article_responses:
    text = BeautifulSoup(data['content'], "html.parser").get_text(separator=' ')

    if (len(text) < 10):
        continue

    knowledge_items.append({
        'category': data['name'],
        'text': text,
        'link': f'https://twork.tinkoff.ru/workspace/knowledge-base/subsection/{data["subsectionId"]}/article/{data["id"]}',
    })

print(knowledge_items)

with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['category', 'text', 'link']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(knowledge_items)