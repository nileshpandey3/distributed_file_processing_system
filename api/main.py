# api/main.py

from fastapi import FastAPI
import redis, uuid, json
import os

app = FastAPI()
r = redis.Redis(host="redis", port=6379, decode_responses=True)

QUEUE = "files_to_process"
STATUS_PREFIX = "job_status:"
RESULTS_PREFIX = "job_results:"
DATA_FOLDER = "./data"


@app.post("/submit")
def submit_job():
    job_id = str(uuid.uuid4())

    files = [os.path.join(DATA_FOLDER, f) for f in os.listdir(DATA_FOLDER)]

    # initialize job
    r.hset(f"{STATUS_PREFIX}{job_id}", "total", len(files))
    r.hset(f"{STATUS_PREFIX}{job_id}", "processed", 0)

    for fpath in files:
        task = json.dumps({"job_id": job_id, "file": fpath})
        r.rpush(QUEUE, task)

    return {"job_id": job_id, "file_count": len(files)}


@app.get("/status/{job_id}")
def job_status(job_id: str):
    return r.hgetall(f"{STATUS_PREFIX}{job_id}")


@app.get("/results/{job_id}")
def job_results(job_id: str):
    results = r.lrange(f"{RESULTS_PREFIX}{job_id}", 0, -1)
    return [json.loads(r) for r in results]
