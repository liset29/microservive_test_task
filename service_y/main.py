import logging

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from service_y.app.handlers import TaskHandler
from service_y.config import RABBITMQ_URL, create_task_queue, start_task_queue

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

broker = RabbitBroker(RABBITMQ_URL)
app = FastStream(broker)


@broker.subscriber(create_task_queue)
async def create_task(msg: dict):
    return await TaskHandler.create_task(msg)


@broker.subscriber(start_task_queue)
async def start_task(msg: dict):
    return await TaskHandler.start_task(msg)