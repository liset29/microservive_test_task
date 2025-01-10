import logging

from faststream import FastStream
from faststream.rabbit import RabbitBroker
from service_y.app.handlers import TaskHandler
from service_y.config import start_task_queue, request_queue, RABBITMQ_URL, create_task_queue, response_queue

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

broker = RabbitBroker(RABBITMQ_URL)
app = FastStream(broker)


@broker.subscriber(create_task_queue)
async def create_task(msg: dict):
    return await TaskHandler.create_task(msg)


@broker.subscriber(start_task_queue)
async def start_task(msg: dict):
    return await TaskHandler.start_task(msg)


@broker.subscriber(request_queue)
async def get_tasks(message: dict):
    print(message)
    if "id" in message:
        response_data = await TaskHandler.get_task(message['id'])
    else:
        response_data = await TaskHandler.get_all_tasks()
    await broker.publish(
        {
            "data": response_data,

            "correlation_id": message.get("correlation_id"),
        },
        queue=response_queue,
    )