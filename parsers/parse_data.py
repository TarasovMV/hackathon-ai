from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor
import csv

# URL для GET-запроса
menu_url = 'https://twork.tinkoff.ru/knowledge-base/api/sections/list?spaceCode=kwb_default_space'
sections_url = 'https://twork.tinkoff.ru/knowledge-base/api/subsections'
article_url = 'https://twork.tinkoff.ru/knowledge-base/api/articles'
# Куки в виде строки
cookie_str = ''
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