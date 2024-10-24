import time
import random
import asyncio
import json
import threading
from flask import Flask, Response, jsonify, stream_with_context
from flask_cors import CORS

import shared_state

# from modules.voicekit_module import voice_recognition
# from modules.articles_module import articles_job
# from modules.procedures_module import procedures_job
# from modules.llm_module import llm_job

from modules.mocks.voicekit_module import voice_recognition
from modules.mocks.articles_module import articles_job
from modules.mocks.procedures_module import procedures_job
from modules.mocks.llm_module import llm_job

app = Flask(__name__)
CORS(app)


app_threads = {
    'voicekit_thread': None,
    'articles_thread': None,
    'procedures_thread': None,
    'llm_thread': None
}

@app.route('/start', methods=['POST'])
def start_jobs():
    global app_threads

    [t.start() for t in app_threads.values()]

    return jsonify({"message": "Ok"}), 200

@app.route('/llm_mock', methods=['POST'])
def llm_mock():
    time.sleep(random.uniform(0, 3))
    return jsonify({"message": "Mock Result"}), 200

# SSE отправка данных
@app.route('/stream')
def sse_stream():
    def event_stream():
        last_sent_data = None

        while True:
            with shared_state.sse_data.data_condition:
                shared_state.sse_data.data_condition.wait()
                # Проверяем, изменились ли данные
                if shared_state.sse_data and shared_state.sse_data != last_sent_data:
                    # Отправляем только если данные изменились
                    message = f"data: {json.dumps(shared_state.sse_data.get())}\n\n"
                    last_sent_data = shared_state.sse_data.get()  # Обновляем последние отправленные данные
                    yield message  # Генерация события для клиента
                # else:
                    # Пустое событие для поддержания активного соединения
                    # yield ":\n\n"
                # time.sleep(0.1)  # Ожидание перед отправкой нового сообщения

    return Response(stream_with_context(event_stream()), content_type='text/event-stream')

# Запуск потоков для gRPC и HTTP запросов к LLM
if __name__ == '__main__':    
    # voicekit_thread = threading.Thread(target=voice_recognition)
    app_threads['voicekit_thread'] = threading.Thread(target=lambda: asyncio.run(voice_recognition()))
    app_threads['articles_thread'] = threading.Thread(target=articles_job)
    app_threads['procedures_thread'] = threading.Thread(target=procedures_job)
    app_threads['llm_thread'] = threading.Thread(target=llm_job)

    app.run(threaded=True)