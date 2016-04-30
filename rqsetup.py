# Configuration file for RQ
# Borrows conf settings from watchman's conf file
import watchman.conf

QUEUES = watchman.conf.QUEUES
REDIS_URL = "redis://{0}:{1}/1".format(watchman.conf.REDIS_HOST, watchman.conf.REDIS_PORT)
