from mpi4py import MPI
import pandas as pd

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

df = pd.read_csv(f"log_chunk_{rank}.csv")

local_stats = {
    "rank": rank,
    "avg_wait_time": df['wait_time'].mean(),
    "avg_runtime": df['runtime'].mean(),
    "max_wait_time": df['wait_time'].max(),
    "job_count": len(df)
}

print(f"Rank {rank}: {local_stats}")

all_stats = comm.gather(local_stats, root=0)

if rank == 0:
    total_jobs = sum(s['job_count'] for s in all_stats)
    avg_wait_time = sum(s['avg_wait_time'] * s['job_count'] for s in all_stats) / total_jobs
    avg_runtime = sum(s['avg_runtime'] * s['job_count'] for s in all_stats) / total_jobs
    max_wait_time = max(s['max_wait_time'] for s in all_stats)

    print(f"\n=== Combined Summary (across {len(all_stats)} chunks, {total_jobs} total jobs) ===")
    print(f"Overall avg wait_time: {avg_wait_time:.2f}")
    print(f"Overall avg runtime: {avg_runtime:.2f}")
    print(f"Overall max wait_time: {max_wait_time:.2f}")
