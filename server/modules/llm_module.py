import time
import shared_state

from utils.proxy_util import proxy_ai
from utils.searchy_util import searchy


job_timeout = 30 # Запросы каждые 30 секунд

def llm_job():
    time.sleep(job_timeout)
    while True:
        if len(shared_state.recognition_data) > 0:
            try:
                start_time = time.time()  # Замер времени начала выполнения блока

                result = proxy_ai(shared_state.recognition_data)
                shared_state.sse_data.set({"type": "llm", "data": result})

                execution_time = time.time() - start_time  # Время выполнения блока

                # Рассчитываем оставшееся время для паузы
                sleep_time = job_timeout - execution_time
                if sleep_time > 0:
                    time.sleep(sleep_time)
            except Exception as e:
                print(f"Error articles_job: {e}")
        else:
            time.sleep(job_timeout)  # Если данных нет, ждем полный таймаут