import os

from redis import Redis
from rq import Queue

redis_conn = Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=6379
)

document_queue = Queue(
    "documents",
    connection=redis_conn
)