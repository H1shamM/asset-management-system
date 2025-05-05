import os
import redis

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")  # Default to localhost for development

redis_client = redis.StrictRedis.from_url(redis_url, decode_responses=True)
