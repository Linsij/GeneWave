import time
import random

from genewave.alignment import smith_waterman


def generate_dna_sequence(length: int, seed: int) -> str:
    """Generate a reproducible random DNA sequence."""
    rng = random.Random(seed)
    return "".join(rng.choices("ACGT", k=length))


def benchmark_alignment(length: int, runs: int = 3) -> dict:
    """Measure Smith-Waterman execution time."""
    sequence1 = generate_dna_sequence(length, seed=42)
    sequence2 = generate_dna_sequence(length, seed=43)

    times = []
    result = None

    for _ in range(runs):
        start = time.perf_counter()
        result = smith_waterman(sequence1, sequence2)
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return {
        "sequence_length": length,
        "runs": runs,
        "average_seconds": sum(times) / runs,
        "minimum_seconds": min(times),
        "alignment_score": result.score,
    }


def main():
    print("GeneWeaver CPU Alignment Benchmark")
    print("=" * 55)

    for length in (100, 250, 500, 1000):
        result = benchmark_alignment(length)

        print(
            f"Length: {result['sequence_length']:>4} | "
            f"Average: {result['average_seconds']:.6f}s | "
            f"Minimum: {result['minimum_seconds']:.6f}s | "
            f"Score: {result['alignment_score']}"
        )


if __name__ == "__main__":
    main()
