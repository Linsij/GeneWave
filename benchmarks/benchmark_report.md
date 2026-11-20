# GeneWeaver CPU Alignment Benchmark

**Date:** November 20, 2026
**Algorithm:** Smith-Waterman Local Alignment
**Implementation:** Python CPU

## 1. Objective

Measure the execution time of the CPU-based Smith-Waterman
algorithm for different DNA sequence lengths.

## 2. Benchmark Configuration

- Sequence lengths: 100, 250, 500, and 1,000 bases
- Runs per sequence length: 3
- Match score: +2
- Mismatch penalty: -1
- Gap penalty: -2
- DNA sequences: Reproducibly generated using fixed random seeds
- Timer: Python time.perf_counter()

## 3. Results

| Sequence Length | Average Time (s) | Minimum Time (s) | Alignment Score |
|---:|---:|---:|---:|
| 100 | 0.003076 | 0.002906 | 43 |
| 250 | 0.022380 | 0.021303 | 105 |
| 500 | 0.124782 | 0.100531 | 210 |
| 1,000 | 0.360348 | 0.332889 | 454 |

## 4. Observations

- Execution time increased with sequence length.
- Larger sequences require more dynamic programming calculations.
- The implementation provides a CPU performance baseline for future GPU comparisons.
- Three runs were performed for each sequence length.

## 5. Conclusion

The CPU-based Smith-Waterman implementation was successfully benchmarked
using four different DNA sequence lengths.

The recorded measurements will serve as a reference for evaluating
future GPU-accelerated alignment implementations.

## 6. Future Work

- Implement GPU-accelerated Smith-Waterman alignment.
- Compare CPU and GPU execution times.
- Evaluate performance on larger genomic sequences.
- Integrate alignment processing with genomic chunking.
