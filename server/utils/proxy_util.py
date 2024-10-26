import requests
import os
from dotenv import load_dotenv


load_dotenv()

access_token = os.environ["OPEN_AI_PROXY"]


def proxy_ai(prompt, system_prompt):
    url = 'https://openai-proxy.tcsbank.ru/public/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token,
        'x-proxy-mask-critical-data': '1'
    }

    data = {
        'model': 'gpt-4o',
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt},
        ]
    }

    # Отправка POST-запроса
    response = requests.post(url, headers=headers, json=data)

    # Проверка статуса ответа
    if response.status_code == 200:
        result = response.json()
        content = result['choices'][0]['message']['content']
        return content
    else:
        raise Exception(f'Ошибка: {response.status_code}, {response.text}')