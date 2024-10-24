import requests

def mock_request(input):
    # Отправка POST-запроса
    response = requests.post('http://localhost:5000/llm_mock', json={})

    # Проверка статуса ответа
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Ошибка: {response.status_code}, {response.text}')