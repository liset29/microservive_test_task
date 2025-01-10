import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
create_task_queue = os.getenv("CREATE_TASK_QUEUE")
start_task_queue = os.getenv("START_TASK_QUEUE")
request_queue = os.getenv("REQUEST_TASK_QUEUE")
response_queue = os.getenv("RESPONSE_TASK_QUEUE")