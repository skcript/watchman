# -*- encoding: utf-8 -*-
# Run using `python watchman/worker.py` in "watchman" folder

# pip install rq-dashboard
# Run `rq-dashboard` and point browser to http://0.0.0.0:9181/

import os
import redis
from conf import REDIS, QUEUES
from rq import Worker, Queue, Connection

def work():
	print("Hello from the worker side.")
	with Connection(REDIS):
		worker = Worker(map(Queue, QUEUES))
		worker.work()
