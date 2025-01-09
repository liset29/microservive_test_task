from faststream.rabbit.fastapi import RabbitRouter

from service_x.config import RABBITMQ_URL, create_task_queue

router = RabbitRouter(RABBITMQ_URL)


@router.post("/create_tasks")
async def create_task(number: str):
    await router.broker.publish({'number': number},
                                queue=create_task_queue)
    return {'status': 'created'}