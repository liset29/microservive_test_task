import asyncio
from fastapi import HTTPException
from service_x.app.state import task_futures


async def create_future(correlation_id: str):
    future = asyncio.Future()
    task_futures[correlation_id] = future
    return future


async def publish_and_wait(router, payload: dict, queue: str):
    correlation_id = payload["correlation_id"]
    future = await create_future(correlation_id)
    await router.broker.publish(payload, queue=queue)
    response = await future
    if response is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return response
