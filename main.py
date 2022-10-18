import asyncio

from fastapi import FastAPI
from consumer import PikaClient
from service import methods_dict
from router import router


class App(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient(self.handle_incoming_message)

    @classmethod
    def handle_incoming_message(cls, method, body: dict):
        methods_dict[method](body=body)


app = App()
app.include_router(router)


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task


