from collections import defaultdict
from typing import Callable, List, Any
from loguru import logger

class InMemoryBus:
    def __init__(self):
        self._subscribers = defaultdict(list)

    def subscribe(self, topic: str, callback: Callable[[Any], None]):
        self._subscribers[topic].append(callback)
        logger.info(f"Subscribed to topic: {topic}")

    def publish(self, topic: str, message: Any):
        logger.info(f"Publishing to {topic}: {message}")
        for callback in self._subscribers[topic]:
            callback(message)
