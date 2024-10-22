import time
import requests
import json
import shared_state

def send_llm_requests():
    while True:
        if len(shared_state.recognition_data) > 0:
            try:
                # Отправляем запросы в LLM сервис
                response = requests.post('http://localhost:5000/llm_mock', json={})

                # Обработка ответов от LLM сервисов
                result = response.json()

                shared_state.sse_data = {"type": "llm", "data": result}

                print(f"Data sent to LLM services: {json.dumps(result)}")

            except Exception as e:
                print(f"Error sending LLM requests: {e}")
        time.sleep(5)  # Запросы каждые 30 секунд