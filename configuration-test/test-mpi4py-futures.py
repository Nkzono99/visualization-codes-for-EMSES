from mpi4py import MPI
from mpi4py.futures import MPIPoolExecutor


def task(item):
    return item * 2


if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    print(f"Hello, world! from rank {rank} out of {size}")
    count = 0

    result_sum = 0

    with MPIPoolExecutor(max_workers=4) as executor:

        items = range(1000)
        
        mapped = list(executor.map(task, items))

        for result in mapped:
            result_sum += result

    print(f'Sum(2*range(1000)) = {result_sum}', count)
