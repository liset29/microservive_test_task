import uuid
from faststream.rabbit.fastapi import RabbitRouter
from starlette import status
from service_x.app.shemas import TaskSchema, AllTasksResponse
from service_x.app.state import task_futures
from service_x.app.utils import publish_and_wait
from service_x.config import (
    start_task_queue,
    create_task_queue,
    request_queue,
    response_queue,
    RABBITMQ_URL,
)

router = RabbitRouter(RABBITMQ_URL, prefix="/tasks", tags=["Tasks"])


@router.post(
    "/create_tasks",
    response_model=TaskSchema,
    description="Endpoint to create a task in Microservice Y",
    response_description="Confirmation of task creation",
    status_code=status.HTTP_201_CREATED,
)
async def create_task(number: int):
    correlation_id = str(uuid.uuid4())
    payload = {"number": number, "correlation_id": correlation_id}
    return await publish_and_wait(router, payload, create_task_queue)


@router.post(
    "/tasks/{id}/start",
    response_model=TaskSchema,
    description="Endpoint to start a task by ID in Microservice Y",
    response_description="Confirmation of task start",
    status_code=status.HTTP_200_OK,
)
async def start_task(id: int):
    correlation_id = str(uuid.uuid4())
    payload = {"id": id, "correlation_id": correlation_id}
    return await publish_and_wait(router, payload, start_task_queue)


@router.get(
    "/get_tasks",
    response_model=AllTasksResponse,
    description="Endpoint to retrieve all tasks and their statuses from Microservice Y",
    response_description="List of all tasks with their statuses",
    status_code=status.HTTP_200_OK,
)
async def get_tasks():
    correlation_id = str(uuid.uuid4())
    payload = {"correlation_id": correlation_id}
    return await publish_and_wait(router, payload, request_queue)


@router.get(
    "/get_task",
    response_model=TaskSchema,
    description="Endpoint to retrieve a specific task by ID from Microservice Y",
    response_description="Details of the requested task",
    status_code=status.HTTP_200_OK,
)
async def get_task(id: int):
    correlation_id = str(uuid.uuid4())
    payload = {"id": id, "correlation_id": correlation_id}
    return await publish_and_wait(router, payload, request_queue)


@router.subscriber(response_queue)
async def handle_response(message: dict):
    correlation_id = message.get("correlation_id")
    if not correlation_id:
        return
    if correlation_id in task_futures:
        task_futures[correlation_id].set_result(message.get("data"))
        del task_futures[correlation_id]
