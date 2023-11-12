from mpi4py import MPI
import random
import time

def parallel_bubble_sort(arr):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    local_arr = arr[rank::size]

    for i in range(len(local_arr)):
        for j in range(0, len(local_arr) - i - 1):
            if local_arr[j] > local_arr[j + 1]:
                local_arr[j], local_arr[j + 1] = local_arr[j + 1], local_arr[j]

    sorted_arr = comm.gather(local_arr, root=0)

    if rank == 0:
        merged_arr = []
        for sub_arr in sorted_arr:
            merged_arr.extend(sub_arr)

        for i in range(len(merged_arr)):
            for j in range(0, len(merged_arr) - i - 1):
                if merged_arr[j] > merged_arr[j + 1]:
                    merged_arr[j], merged_arr[j + 1] = merged_arr[j + 1], merged_arr[j]

        return merged_arr

if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        n = 10  # Jumlah elemen dalam daftar
        unsorted_list = [random.randint(1, 100) for _ in range(n)]
    else:
        unsorted_list = None

    unsorted_list = comm.bcast(unsorted_list, root=0)

    start_time = time.time()

    sorted_list = parallel_bubble_sort(unsorted_list)

    end_time = time.time()

    if rank == 0:
        print("Daftar sebelum diurutkan:", unsorted_list)
        print("Daftar setelah diurutkan:", sorted_list)
        execution_time = end_time - start_time
        print("Waktu Eksekusi : {:.6f} detik".format(execution_time))
