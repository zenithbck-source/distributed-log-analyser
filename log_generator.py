import random
import pandas as pd

def generate_log_chunks(total_jobs, num_chunks, seed=42):
    jobs = []

    for i in range(1, total_jobs+1):
        job_id = (f"J{i:00005d}")
        submit_time = random.randint(0, 10000)
        runtime = random.randint(1, 20)
        ncpus = random.choice([1,2,4])
        wait_time = random.randint(0, 100)
        jobs.append({"job_id":job_id, "submit_time":submit_time, "runtime":runtime, "ncpus":ncpus, "wait_time":wait_time})

    chunk_size = total_jobs // num_chunks
    chunk_start = 0

    for i in range(0, num_chunks):
        chunk_jobs = jobs[chunk_start:chunk_start+chunk_size]
        df = pd.DataFrame(chunk_jobs)
        df.to_csv(f"log_chunk_{i}")
        print(f"Created log_chunk_{i}.csv.")
        chunk_start += chunk_size



if __name__ == "__main__":
    generate_log_chunks(1000, 4)
