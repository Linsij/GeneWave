
import random
import time

from genewave.alignment import smith_waterman
from genewave.cuda_alignment import cuda_smith_waterman


def generate_sequence(length, seed):
    rng = random.Random(seed)
    return "".join(rng.choices("ACGT", k=length))


def benchmark():
    print("GeneWeaver CPU vs GPU Smith-Waterman Benchmark")
    print("=" * 55)

    # Warm up the GPU before measuring execution time
    cuda_smith_waterman("ACGT", "ACGT")

    lengths = [100, 250, 500, 1000]
    runs = 3

    print(f"\nRuns per sequence length: {runs}\n")

    for length in lengths:
        sequence1 = generate_sequence(length, 42)
        sequence2 = generate_sequence(length, 43)

        cpu_times = []
        gpu_times = []

        for _ in range(runs):
            start = time.perf_counter()
            cpu_result = smith_waterman(sequence1, sequence2)
            cpu_times.append(time.perf_counter() - start)

            start = time.perf_counter()
            gpu_result = cuda_smith_waterman(sequence1, sequence2)
            gpu_times.append(time.perf_counter() - start)

            if cpu_result != gpu_result:
                raise AssertionError(
                    f"CPU/GPU mismatch for sequence length {length}"
                )

        cpu_average = sum(cpu_times) / runs
        gpu_average = sum(gpu_times) / runs

        print(f"Sequence length: {length}")
        print(f"CPU average: {cpu_average:.6f} seconds")
        print(f"GPU average: {gpu_average:.6f} seconds")
        print(f"Alignment score: {cpu_result.score}")

        if gpu_average > 0:
            ratio = cpu_average / gpu_average
            print(f"CPU/GPU time ratio: {ratio:.2f}x")

        print("-" * 55)


if __name__ == "__main__":
    benchmark()
