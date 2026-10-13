from src.config import settings
from src.connectors.redis_connectors import RedisConnector

redis_manager = RedisConnector(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
