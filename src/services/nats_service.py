import json
import asyncio
from nats.aio.client import Client as NATS
from typing import Callable

class NatsService:
    def __init__(self, nats_url: str):
        self.nats_url = nats_url
        self.nc = NATS()
        
    async def connect(self):
        await self.nc.connect(self.nats_url)
        
    async def subscribe(self, subject: str, callback: Callable):
        await self.nc.subscribe(subject, cb=callback)
        
    async def publish(self, subject: str, message: dict):
        await self.nc.publish(subject, json.dumps(message).encode()) 