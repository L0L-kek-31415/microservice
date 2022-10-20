import asyncio

from fastapi import FastAPI
from consumer import PikaClient
from router import router


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
