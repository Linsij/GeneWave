

\# GeneWeaver GPU Smith-Waterman Benchmark Report



\*\*Date:\*\* November 23, 2026

\*\*Algorithm:\*\* Smith-Waterman Local Alignment

\*\*CPU Implementation:\*\* Python

\*\*GPU Implementation:\*\* Numba CUDA with anti-diagonal processing

\*\*GPU:\*\* NVIDIA GeForce GTX 1650 (4 GB)



\## 1. Objective



Evaluate the correctness and execution performance of the

GPU-accelerated Smith-Waterman alignment implementation

against the existing CPU implementation.



\## 2. Benchmark Configuration



\- Sequence lengths: 100, 250, 500, and 1,000 bases

\- Runs per sequence length: 3

\- DNA bases: A, C, G, T

\- Reproducible random sequences using seeds 42 and 43

\- Timing: Python time.perf\_counter()

\- GPU warm-up performed before measurements

\- CPU/GPU results compared for correctness



\## 3. Benchmark Results



| Sequence Length | CPU Average (s) | GPU Average (s) | CPU/GPU Ratio |

|---:|---:|---:|---:|

| 100 | 0.005183 | 0.034924 | 0.15x |

| 250 | 0.025221 | 0.046142 | 0.55x |

| 500 | 0.084035 | 0.072174 | 1.16x |

| 1,000 | 0.337974 | 0.135353 | 2.50x |



\## 4. Observations



\- CPU execution was faster for sequence lengths of 100 and 250.

\- GPU execution became faster at 500 bases.

\- At 1,000 bases, GPU execution achieved approximately

&#x20; 2.50x the CPU/GPU performance ratio.

\- GPU kernel-launch overhead affects smaller workloads.

\- CPU and GPU alignment results matched for every benchmark.



\## 5. Implementation Details



The GPU implementation calculates the Smith-Waterman

scoring matrix using anti-diagonal wavefront processing.



Each anti-diagonal is processed in a separate CUDA kernel

launch to ensure dependent cells are calculated in the

correct order.



The scoring matrix is copied back to the CPU, where

traceback reconstructs the final local alignment.



\## 6. Conclusion



The GPU implementation passed correctness comparisons

against the CPU implementation.



Initial measurements show that GPU execution becomes

beneficial for the larger tested sequences, reaching an

approximately 2.50x performance ratio at 1,000 bases.



Further optimization is needed to reduce kernel-launch

overhead and improve GPU utilization.



\## 7. Future Improvements



\- Reduce the number of CUDA kernel launches.

\- Improve GPU occupancy and parallel workload distribution.

\- Benchmark longer DNA sequences.

\- Investigate tiled wavefront processing.

\- Evaluate performance across additional sequence sizes.
