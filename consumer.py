import json

import pika
from aio_pika import connect_robust


class PikaClient:

    def __init__(self, process_callable):
        self.publish_queue_name = "statistics"
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq")
        )
        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(queue=self.publish_queue_name)
        self.callback_queue = self.publish_queue.method.queue
        self.response = None
        self.process_callable = process_callable

    async def consume(self, loop):
        """Setup message listener with the current running loop"""
        connection = await connect_robust(host="rabbitmq",
                                          port=5672,
                                          loop=loop)
        channel = await connection.channel()
        queue = await channel.declare_queue("statistics")
        await queue.consume(self.process_incoming_message, no_ack=False)
        return connection

    async def process_incoming_message(self, message):
        """Processing incoming message from RabbitMQ"""
        message.ack()
        body = message.body
        if body:
            self.process_callable(json.loads(body))

