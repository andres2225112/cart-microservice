import os
import redis.asyncio as aioredis
from dotenv import load_dotenv

load_dotenv()

redis_client: aioredis.Redis | None = None

async def connect_redis():
    global redis_client
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    try:
        redis_client = aioredis.from_url(redis_url, decode_responses=True)
        await redis_client.ping()
        print("✅ Redis connection successful")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")

async def disconnect_redis():
    global redis_client
    if redis_client:
        await redis_client.close()

def get_redis() -> aioredis.Redis:
    return redis_client
