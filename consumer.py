import json

import pika
import aio_pika
from service import methods_dict


class PikaClient:
    def __init__(self):
        self.publish_queue_name = "statistics"
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="rabbitmq", heartbeat=600, blocked_connection_timeout=300
            )
        )
        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(queue=self.publish_queue_name)
        self.callback_queue = self.publish_queue.method.queue
        self.response = None

    @classmethod
    def handle_incoming_message(cls, body: dict):

        methods_dict[body["method"]](body=body)

    async def consume(self, loop):
        """Setup message listener with the current running loop"""
        connection = await aio_pika.connect_robust(
            host="rabbitmq", port=5672, loop=loop
        )
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=100)
        queue = await channel.declare_queue(self.publish_queue_name)
        await queue.consume(self.process_incoming_message)
        return connection

    @staticmethod
    async def process_incoming_message(message) -> None:
        """Processing incoming message from RabbitMQ"""
        async with message.process():
            print(message.body)
            PikaClient.handle_incoming_message(json.loads(message.body))
