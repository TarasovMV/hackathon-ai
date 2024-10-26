import time
import shared_state

from utils.proxy_util import proxy_ai
from utils.searchy_util import searchy
from prompts.agent_prompt import agent_prompt


job_timeout = 30 # Запросы каждые 30 секунд
searchy_indexes = ["tidy-shrimp-1729889539"]

def procedures_job():
    time.sleep(job_timeout)
    while True:
        if len(shared_state.recognition_data) > 0:
            try:
                start_time = time.time()  # Замер времени начала выполнения блока

                prompt = ", ".join(shared_state.recognition_data)

                search_str = proxy_ai(prompt, agent_prompt)
                result = searchy(search_str, searchy_indexes)
                shared_state.sse_data.set({"type": "procedure", "data": result})

                execution_time = time.time() - start_time  # Время выполнения блока

                # Рассчитываем оставшееся время для паузы
                sleep_time = job_timeout - execution_time
                if sleep_time > 0:
                    time.sleep(sleep_time)
            except Exception as e:
                print(f"Error articles_job: {e}")
                time.sleep(job_timeout)
        else:
            time.sleep(job_timeout)  # Если данных нет, ждем полный таймаут