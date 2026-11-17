import numpy as np
from numba import cuda


@cuda.jit
def add_ten_kernel(input_array, output_array):
    index = cuda.grid(1)

    if index < input_array.size:
        output_array[index] = input_array[index] + 10


def test_cuda_add_ten():
    assert cuda.is_available(), "CUDA GPU is not available"

    host_input = np.arange(100, dtype=np.int32)
    host_output = np.zeros_like(host_input)

    device_input = cuda.to_device(host_input)
    device_output = cuda.device_array_like(host_output)

    threads_per_block = 128
    blocks_per_grid = (
        host_input.size + threads_per_block - 1
    ) // threads_per_block

    add_ten_kernel[blocks_per_grid, threads_per_block](
        device_input,
        device_output,
    )

    cuda.synchronize()

    result = device_output.copy_to_host()

    np.testing.assert_array_equal(
        result,
        host_input + 10,
    )