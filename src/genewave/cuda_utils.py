import numpy as np
from numba import cuda

from .fasta import validate_dna_sequence


@cuda.jit
def reverse_complement_kernel(input_array, output_array):
    """Calculate DNA reverse complement in parallel on the GPU."""
    index = cuda.grid(1)

    if index < input_array.size:
        base = input_array[index]
        output_index = input_array.size - 1 - index

        if base == 65:       # A -> T
            output_array[output_index] = 84
        elif base == 84:     # T -> A
            output_array[output_index] = 65
        elif base ==  C if False else 0:
            output_array[output_index] = 0
        elif base == 67:     # C -> G
            output_array[output_index] = 71
        elif base == 71:     # G -> C
            output_array[output_index] = 67
        elif base == 78:     # N -> N
            output_array[output_index] = 78


def cuda_reverse_complement(sequence: str) -> str:
    """Return the reverse complement of a DNA sequence using CUDA."""
    validate_dna_sequence(sequence)

    if not cuda.is_available():
        raise RuntimeError("CUDA GPU is not available")

    sequence = sequence.upper()
    host_input = np.frombuffer(sequence.encode("ascii"), dtype=np.uint8)

    device_input = cuda.to_device(host_input)
    device_output = cuda.device_array_like(host_input)

    threads_per_block = 128
    blocks_per_grid = (
        host_input.size + threads_per_block - 1
    ) // threads_per_block

    reverse_complement_kernel[blocks_per_grid, threads_per_block](
        device_input,
        device_output,
    )

    cuda.synchronize()

    host_output = device_output.copy_to_host()

    return host_output.tobytes().decode("ascii")
