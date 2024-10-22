import requests

def search_articles(input):
    # URL для POST-запроса
    url = 'https://searchy-back.tcsgroup.io/v2/docs/search'

    # Данные для отправки в формате JSON
    data = {
        "index_type": "elasticsearch",
        "login": "m.tarasov",
        "project": "hakaton_ai_test",
        "where": [
            "opalescent-cuttlefish-1729268026"
        ],
        "query": {
            "text": input
        },
        "top_n": 5,
        "threshold": 0.5,
        "include_embedding": False
    }

    # Отправка POST-запроса
    response = requests.post(url, json=data, verify=False)

    # Проверка статуса ответа
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Ошибка: {response.status_code}, {response.text}')
    
result = search_articles('вклад')

print(result.get('result', [])[0])