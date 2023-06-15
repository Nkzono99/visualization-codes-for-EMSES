from mpi4py import MPI
from mpi4py.futures import MPIPoolExecutor


if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    print(f"Hello, world! from rank {rank} out of {size}")
