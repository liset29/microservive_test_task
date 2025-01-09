from fastapi import FastAPI

from service_x.app.routes import router

app = FastAPI()
app.include_router(router)
