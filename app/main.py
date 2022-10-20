import asyncio

from fastapi import FastAPI

from app.services.consumer import PikaClient
from app.services.router import router


class App(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient()


app = App()
app.include_router(router)


@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task
