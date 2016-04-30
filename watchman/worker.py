# Run using `python watchman/worker.py` in "watchman" folder
# Even better!
# Run using `rq worker -c rqsetup` in "watchman" folder
import os
import redis
from conf import REDIS, QUEUES
from rq import Worker, Queue, Connection

print("Hello from the worker sideeeee.")
with Connection(REDIS):
	worker = Worker(map(Queue, QUEUES))
	worker.work()
