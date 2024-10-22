import time
import asyncio
import json
import threading
from flask import Flask, Response, jsonify, stream_with_context
from flask_cors import CORS

import shared_state
from server.viocekit_test_module import grpc_stream
from server.request_test_module import send_llm_requests
from voicekit_module import voice_recognition

app = Flask(__name__)
CORS(app)

@app.route('/llm_mock', methods=['POST'])
def llm_mock():
    return jsonify({"message": "LLM Result"}), 200

# SSE отправка данных
@app.route('/stream')
def sse_stream():
    def event_stream():
        last_sent_data = None

        while True:
            # Проверяем, изменились ли данные
            if shared_state.sse_data and shared_state.sse_data != last_sent_data:
                # Отправляем только если данные изменились
                message = f"data: {json.dumps(shared_state.sse_data)}\n\n"
                last_sent_data = shared_state.sse_data  # Обновляем последние отправленные данные
                yield message  # Генерация события для клиента
            else:
                # Пустое событие для поддержания активного соединения
                yield ":\n\n"
            time.sleep(1)  # Ожидание перед отправкой нового сообщения

    return Response(stream_with_context(event_stream()), content_type='text/event-stream')

# Запуск потоков для gRPC и HTTP запросов к LLM
if __name__ == '__main__':
    # voicekit_thread = threading.Thread(target=voice_recognition)
    # voicekit_thread.start()

    grpc_thread = threading.Thread(target=lambda: asyncio.run(grpc_stream()))
    grpc_thread.start()

    llm_thread = threading.Thread(target=send_llm_requests)
    llm_thread.start()

    app.run(threaded=True)