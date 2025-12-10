import time

import redis


def connect_redis():
    while True:
        try:
            return redis.Redis(host='localhost', port=6379, decode_responses=True)
        except Exception as e:
            print(f"Redis connection error: {e}, retrying")
            time.sleep(3)
            continue

r = connect_redis()

# Redis store keys for jobs to process and results
QUEUE = 'files_to_process'
RESULTS = 'job_results'

while True:
    try:
        job = r.lpop(QUEUE)
    except redis.exceptions.ConnectionError as e:
        print("Lost connection to Redis — reconnecting....", e)
        r = connect_redis()
        continue

