from rq import Worker
from rq import Queue
from app.core.redis import redis_conn

worker = Worker(
    [
        Queue(
            "documents",
            connection=redis_conn
        )
    ]
)

worker.work()