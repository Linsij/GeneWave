
import numpy as np
from numba import cuda

from .alignment import AlignmentResult
from .fasta import validate_dna_sequence


@cuda.jit
def _smith_waterman_diagonal(
    sequence1,
    sequence2,
    matrix,
    diagonal,
    rows,
    columns,
    match_score,
    mismatch_score,
    gap_penalty,
):
    index = cuda.grid(1)

    min_i = max(1, diagonal - (columns - 1))
    max_i = min(rows - 1, diagonal - 1)

    i = min_i + index

    if i <= max_i:
        j = diagonal - i

        if sequence1[i - 1] == sequence2[j - 1]:
            substitution = match_score
        else:
            substitution = mismatch_score

        diagonal_score = matrix[i - 1, j - 1] + substitution
        up_score = matrix[i - 1, j] + gap_penalty
        left_score = matrix[i, j - 1] + gap_penalty

        score = max(0, diagonal_score, up_score, left_score)
        matrix[i, j] = score


def cuda_smith_waterman(
    sequence1: str,
    sequence2: str,
    match_score: int = 2,
    mismatch_score: int = -1,
    gap_penalty: int = -2,
) -> AlignmentResult:
    """Perform Smith-Waterman scoring on the GPU and traceback on the CPU."""

    # Validate input DNA sequences
    validate_dna_sequence(sequence1)
    validate_dna_sequence(sequence2)

    # Validate scoring parameters
    parameters = (match_score, mismatch_score, gap_penalty)

    if any(
        not isinstance(value, int) or isinstance(value, bool)
        for value in parameters
    ):
        raise TypeError("Alignment scores must be integers.")

    if match_score <= 0:
        raise ValueError("Match score must be positive.")

    if mismatch_score > 0 or gap_penalty > 0:
        raise ValueError("Mismatch and gap penalties must not be positive.")

    if not cuda.is_available():
        raise RuntimeError("CUDA GPU is not available.")

    sequence1 = sequence1.upper()
    sequence2 = sequence2.upper()

    # Convert DNA sequences into NumPy arrays
    host_seq1 = np.frombuffer(sequence1.encode("ascii"), dtype=np.uint8)
    host_seq2 = np.frombuffer(sequence2.encode("ascii"), dtype=np.uint8)

    rows = len(sequence1) + 1
    columns = len(sequence2) + 1

    # Initialize scoring matrix
    host_matrix = np.zeros((rows, columns), dtype=np.int32)

    if len(sequence1) == 0 or len(sequence2) == 0:
        return AlignmentResult(0, "", "", 0, 0, 0, 0)

    # Transfer data to GPU
    device_seq1 = cuda.to_device(host_seq1)
    device_seq2 = cuda.to_device(host_seq2)
    device_matrix = cuda.to_device(host_matrix)

    threads_per_block = 128

    # Calculate the scoring matrix using anti-diagonal processing
    for diagonal in range(2, rows + columns - 1):
        min_i = max(1, diagonal - (columns - 1))
        max_i = min(rows - 1, diagonal - 1)
        cell_count = max_i - min_i + 1

        if cell_count > 0:
            blocks = (
                cell_count + threads_per_block - 1
            ) // threads_per_block

            _smith_waterman_diagonal[blocks, threads_per_block](
                device_seq1,
                device_seq2,
                device_matrix,
                diagonal,
                rows,
                columns,
                match_score,
                mismatch_score,
                gap_penalty,
            )

    # Synchronize GPU execution and copy matrix back to CPU
    cuda.synchronize()
    host_matrix = device_matrix.copy_to_host()

    # Find the highest alignment score
    best_position = np.unravel_index(
        np.argmax(host_matrix),
        host_matrix.shape,
    )

    best_score = int(host_matrix[best_position])
    i, j = best_position

    end1, end2 = i, j

    aligned1 = []
    aligned2 = []

    # Traceback on CPU
    while i > 0 and j > 0 and host_matrix[i, j] > 0:
        current = host_matrix[i, j]

        diagonal_score = (
            host_matrix[i - 1, j - 1]
            + (
                match_score
                if sequence1[i - 1] == sequence2[j - 1]
                else mismatch_score
            )
        )

        up_score = host_matrix[i - 1, j] + gap_penalty
        left_score = host_matrix[i, j - 1] + gap_penalty

        if current == diagonal_score:
            aligned1.append(sequence1[i - 1])
            aligned2.append(sequence2[j - 1])
            i -= 1
            j -= 1

        elif current == up_score:
            aligned1.append(sequence1[i - 1])
            aligned2.append("-")
            i -= 1

        elif current == left_score:
            aligned1.append("-")
            aligned2.append(sequence2[j - 1])
            j -= 1

        else:
            break

    # Return the complete alignment result
    return AlignmentResult(
        score=int(best_score),
        aligned_sequence1="".join(reversed(aligned1)),
        aligned_sequence2="".join(reversed(aligned2)),
        start1=int(i),
        end1=int(end1),
        start2=int(j),
        end2=int(end2),
    )
