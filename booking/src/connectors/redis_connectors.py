# redis_connector.py
import redis.asyncio as redis


class RedisConnector:
    host: str
    port: int
    client: redis.Redis

    def __init__(self, host="localhost", port=6379):
        self.host = host
        self.port = port

    async def connect(self):
        self.client = await redis.Redis(host=self.host, port=self.port, decode_responses=False)

    async def get(self, key):
        return await self.client.get(key)

    async def set(self, key, value, expire: int = None):
        if expire:
            await self.client.set(key, value, ex=expire)
        else:
            await self.client.set(key, value)

    async def delete(self, key):
        return await self.client.delete(key)

    async def close(self):
        if self.client:
            await self.client.close()
