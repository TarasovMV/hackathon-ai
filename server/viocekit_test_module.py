import asyncio
import time

import shared_state

async def grpc_stream():
    while True:
        # Симуляция получения данных из gRPC
        mock = {"type": "chat", "message": f"new grpc data {time.time()}"}

        shared_state.sse_data = mock
        shared_state.recognition_message = mock
        shared_state.recognition_data.append(mock)
        
        await asyncio.sleep(1)  # Симуляция потока gRPC