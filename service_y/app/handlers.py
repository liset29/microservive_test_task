import logging

from service_y.app.db.database import db_session
from service_y.app.db.models import Task


class TaskHandler:
    @staticmethod
    async def create_task(data: dict):
        try:
            logging.info(f"Создание задачи с данными: {data}")
            task = Task(status="created", number=data['number'])
            db_session.add(task)
            db_session.commit()
            logging.info(f"Задача создана: {task.id} со статусом {task.status}")
            return {"id": task.id, "status": task.status}
        except Exception as e:
            logging.error(f"Ошибка при создании задачи: {e}")
            raise
