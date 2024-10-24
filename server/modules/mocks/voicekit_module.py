import asyncio
import time

import shared_state

async def voice_recognition():
    while True:
        # Симуляция получения данных из gRPC
        mock = {"type": "chat", "message": f"new grpc data {time.time()}"}

        shared_state.recognition_message = mock
        shared_state.recognition_data.append(mock)
        shared_state.sse_data.set(mock)
        
        await asyncio.sleep(1)  # Симуляция потока gRPC