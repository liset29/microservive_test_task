import asyncio
import logging

from service_y.app.calc_fibonacci import fibonacci
from service_y.app.db.database import db_session
from service_y.app.db.models import Task
from service_y.app.shemas import TaskSchema, AllTasksResponse


class TaskHandler:
    @staticmethod
    async def create_task(number: int) -> TaskSchema:
        try:
            logging.info(f"Создание задачи с данными: {number}")
            task = Task(status="created", number=number)
            db_session.add(task)
            db_session.commit()
            task = TaskSchema.model_validate(task)
            return task
        except Exception as e:
            logging.error(f"Ошибка при создании задачи: {e}")
            raise

    @staticmethod
    async def start_task(task_id) -> TaskSchema:
        try:
            logging.info(f"Запуск задачи с ID: {task_id}")

            task = db_session.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status = "in_progress"
                db_session.commit()
                logging.info(f"Статус задачи {task_id} обновлен на 'in_progress'")

                asyncio.create_task(TaskHandler.compute_task(task_id, task.number))
                task = TaskSchema.model_validate(task)
                return task

            logging.warning(f"Задача с ID {task_id} не найдена.")
            return {"error": "Task not found"}
        except Exception as e:
            logging.error(f"Ошибка при запуске задачи: {e}")
            raise

    @staticmethod
    async def compute_task(task_id: int, number: int):
        try:
            result = await asyncio.to_thread(fibonacci, number)
            task = db_session.query(Task).filter(Task.id == task_id).first()
            if task:
                task.result = result
                task.status = 'completed'
                db_session.commit()
                logging.info(f"Задача {task_id} завершена со статусом 'completed' и результатом {result}")
        except Exception as e:
            logging.error(f"Ошибка при вычислении задачи {task_id}: {e}")

    @staticmethod
    async def get_all_tasks() -> AllTasksResponse:
        tasks = db_session.query(Task).all()
        tasks_info = [TaskSchema.model_validate(task) for task in tasks]
        return AllTasksResponse(tasks=tasks_info)

    @staticmethod
    async def get_task(task_id: int) -> TaskSchema:
        task = db_session.query(Task).filter(Task.id == task_id).first()
        if not task:
            return None
        return TaskSchema.model_validate(task)
