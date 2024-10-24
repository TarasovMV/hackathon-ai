from threading import Condition

class SseData():
    data_condition = Condition()
    data = None

    @classmethod
    def set(cls, value):
        with cls.data_condition:
            cls.data = value
            cls.data_condition.notify_all()

    @classmethod
    def get(cls):
        return cls.data

sse_data = SseData()
recognition_message = None
recognition_data = []