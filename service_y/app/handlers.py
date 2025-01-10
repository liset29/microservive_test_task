import logging

from service_y.app.db.database import db_session
from service_y.app.calc_fibonacci import fibonacci
from service_y.app.db.models import Task
from service_y.app.shemas import TaskSchema, AllTasksResponse


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

    @staticmethod
    async def start_task(data: dict):
        try:
            task_id = data["id"]
            logging.info(f"Запуск задачи с ID: {task_id}")

            task = db_session.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status = "in_progress"
                db_session.commit()
                logging.info(f"Статус задачи {task_id} обновлен на 'in_progress'")

                result = fibonacci(task.number)
                task.result = result
                task.status = 'completed'
                db_session.commit()
                logging.info(f"Задача {task_id} завершена со статусом 'completed' и результатом {result}")
                return {"id": task_id, "status": task.status, "result": result}

            logging.warning(f"Задача с ID {task_id} не найдена.")
            return {"error": "Task not found"}
        except Exception as e:
            logging.error(f"Ошибка при запуске задачи: {e}")
            raise

    @staticmethod
    async def get_all_tasks() -> AllTasksResponse:
        try:
            logging.info("Получение всех задач.")
            tasks = db_session.query(Task).all()
            tasks_info = [TaskSchema.model_validate(task) for task in tasks]
            logging.info(f"Найдено {len(tasks_info)} задач.")
            tasks_info = AllTasksResponse(tasks=tasks_info)
            return tasks_info
        except Exception as e:
            logging.error(f"Ошибка при получении всех задач: {e}")
            raise

    @staticmethod
    async def get_task(id) -> TaskSchema:
        try:
            logging.info(f"Запрос на получение задачи с id: {id}")

            task = db_session.query(Task).filter(Task.id == id).first()

            if not task:
                logging.warning(f"Задача с id {id} не найдена.")
                return None

            task_data = TaskSchema.model_validate(task)

            logging.info(f"Задача с id {id} получена: {task_data}")
            return task_data
        except Exception as e:
            logging.error(f"Ошибка при получении задачи с id {id}: {e}")
            raise e