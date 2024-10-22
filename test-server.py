import time
import asyncio
import threading
from flask import Flask, Response, jsonify, stream_with_context
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Глобальная переменная для хранения данных из gRPC потока
grpc_data = None
last_sent_data = None  # Храним последние отправленные данные для проверки

# Получаем данные из gRPC
async def grpc_stream():
    global grpc_data
    while True:
        # Симуляция получения новых данных из gRPC
        grpc_data = {"data": f"new grpc data {time.time()}"}
        await asyncio.sleep(5)  # Симуляция потока gRPC

# SSE отправка данных
@app.route('/stream')
def sse_stream():
    def event_stream():
        global grpc_data, last_sent_data
        while True:
            # Проверяем, изменились ли данные
            if grpc_data and grpc_data != last_sent_data:
                # Отправляем только если данные изменились
                message = f"data: {json.dumps(grpc_data)}\n\n"
                last_sent_data = grpc_data  # Обновляем последние отправленные данные
                yield message  # Генерация события для клиента
            else:
                # Пустое событие для поддержания активного соединения
                yield ":\n\n"
            time.sleep(1)  # Ожидание перед отправкой нового сообщения

    return Response(stream_with_context(event_stream()), content_type='text/event-stream')

# Функция для отправки HTTP POST запросов
def send_llm_requests():
    global grpc_data, last_sent_data  # Объявляем глобальную переменную
    while True:
        if grpc_data and grpc_data != last_sent_data:
            try:
                # Отправляем запросы в оба LLM сервиса
                response1 = requests.post('http://llm-service-1/api', json=grpc_data)
                response2 = requests.post('http://llm-service-2/api', json=grpc_data)

                # Логика обработки ответов может быть добавлена здесь
                llm_data = {
                    "llm_service_1_response": response1.json(),
                    "llm_service_2_response": response2.json()
                }
                
                # Обновляем последние отправленные данные
                last_sent_data = grpc_data

                print(f"Data sent to LLM services: {llm_data}")

            except Exception as e:
                print(f"Error sending LLM requests: {e}")
        time.sleep(30)  # Запросы каждые 30 секунд

# Запуск потоков для gRPC и HTTP запросов к LLM
if __name__ == '__main__':
    grpc_thread = threading.Thread(target=lambda: asyncio.run(grpc_stream()))
    grpc_thread.start()

    llm_thread = threading.Thread(target=send_llm_requests)
    llm_thread.start()

    app.run(threaded=True)