# Описание проекта

Проект представляет собой реализацию двух микросервисов `X` и `Y`. Микросервис `Y` отвечает за выполнение трудоёмких математических расчётов, а микросервис `X` предоставляет интерфейс для взаимодействия с микросервисом `Y` через API.

---

## Функционал

### Микросервис `Y`
1. **Создание и сохранение задачи в базе данных** с уникальным идентификатором (`id`).
2. **Запуск расчёта задачи** по её `id`.
3. **Получение результатов и статуса задачи** по её `id`.
4. **Получение списка всех задач** с их статусами и результатами.
5. Реализация через библиотеку **FastStream** и брокер сообщений **RabbitMQ**.

### Микросервис `X`
1. **Создание задачи в микросервисе `Y`** через API (с использованием FastStream).
2. **Запуск задачи по её `id`
3. **Получение результатов и статуса всех задач**.
4. Реализация через **FastAPI**.