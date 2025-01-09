from faststream.rabbit.fastapi import RabbitRouter

from service_x.config import RABBITMQ_URL, create_task_queue, start_task_queue

router = RabbitRouter(RABBITMQ_URL)


@router.post("/create_tasks")
async def create_task(number: int):
    await router.broker.publish({'number': number},
                                queue=create_task_queue)
    return {'status': 'created'}


@router.post("/tasks/{id}/start")
async def start_task(id: int):
    await router.broker.publish({"id": id},
                                queue=start_task_queue)
    return {"message": "Task started"}
