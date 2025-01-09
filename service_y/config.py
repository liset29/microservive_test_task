import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
create_task_queue = os.getenv("CREATE_TASK_QUEUE")
start_task_queue = os.getenv("START_TASK_QUEUE")
