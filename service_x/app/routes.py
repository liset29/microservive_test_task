import uuid
import asyncio
from fastapi import HTTPException
from faststream.rabbit.fastapi import RabbitRouter
from starlette import status
from service_x.app.shemas import TaskSchema, AllTasksResponse
from service_x.config import start_task_queue, create_task_queue, request_queue, response_queue, RABBITMQ_URL

router = RabbitRouter(RABBITMQ_URL,prefix="/tasks", tags=["Tasks"])

task_futures = {}


@router.post(
    "/create_tasks",
    response_model=dict,
    description="Endpoint to create a task in Microservice Y",
    response_description="Confirmation of task creation",
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_task(number: int):
    await router.broker.publish({'number': number}, queue=create_task_queue)
    return {'status': 'created'}

@router.post(
    "/tasks/{id}/start",
    response_model=dict,
    description="Endpoint to start a task by ID in Microservice Y",
    response_description="Confirmation of task start",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def start_task(id: int):
    await router.broker.publish({"id": id}, queue=start_task_queue)
    return {"message": "Task started"}

@router.get(
    "/get_tasks",
    response_model=AllTasksResponse,
    description="Endpoint to retrieve all tasks and their statuses from Microservice Y",
    response_description="List of all tasks with their statuses",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def get_tasks():
    correlation_id = str(uuid.uuid4())
    future = asyncio.Future()
    task_futures[correlation_id] = future

    await router.broker.publish(
        {"correlation_id": correlation_id},
        queue=request_queue,
    )

    response = await future
    return response

@router.get(
    '/get_task',
    response_model=TaskSchema,
    description="Endpoint to retrieve a specific task by ID from Microservice Y",
    response_description="Details of the requested task",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def get_task(id: int):
    correlation_id = str(uuid.uuid4())
    future = asyncio.Future()
    task_futures[correlation_id] = future

    await router.broker.publish(
        {"id": id, "correlation_id": correlation_id},
        queue=request_queue,
    )

    response = await future
    if response is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return response


@router.subscriber(response_queue)
async def handle_response(message: dict):
    correlation_id = message.get("correlation_id")

    if correlation_id in task_futures:
        task_futures[correlation_id].set_result(message.get("data"))
        del task_futures[correlation_id]
