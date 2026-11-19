from dataclasses import dataclass

from .fasta import validate_dna_sequence


@dataclass
class AlignmentResult:
    """Result of a Smith-Waterman local sequence alignment."""

    score: int
    aligned_sequence1: str
    aligned_sequence2: str
    start1: int
    end1: int
    start2: int
    end2: int


def smith_waterman(
    sequence1: str,
    sequence2: str,
    match_score: int = 2,
    mismatch_score: int = -1,
    gap_penalty: int = -2,
) -> AlignmentResult:
    """Perform Smith-Waterman local alignment of two DNA sequences."""

    validate_dna_sequence(sequence1)
    validate_dna_sequence(sequence2)

    scores = (match_score, mismatch_score, gap_penalty)

    if any(
        not isinstance(value, int) or isinstance(value, bool)
        for value in scores
    ):
        raise TypeError("Alignment scores must be integers.")

    if match_score <= 0:
        raise ValueError("Match score must be positive.")

    if mismatch_score > 0 or gap_penalty > 0:
        raise ValueError("Mismatch and gap penalties must not be positive.")

    sequence1 = sequence1.upper()
    sequence2 = sequence2.upper()

    rows = len(sequence1) + 1
    columns = len(sequence2) + 1

    matrix = [[0] * columns for _ in range(rows)]
    traceback = [[None] * columns for _ in range(rows)]

    best_score = 0
    best_position = (0, 0)

    for i in range(1, rows):
        for j in range(1, columns):
            substitution = (
                match_score
                if sequence1[i - 1] == sequence2[j - 1]
                else mismatch_score
            )

            diagonal = matrix[i - 1][j - 1] + substitution
            up = matrix[i - 1][j] + gap_penalty
            left = matrix[i][j - 1] + gap_penalty

            best = max(0, diagonal, up, left)
            matrix[i][j] = best

            if best == 0:
                traceback[i][j] = None
            elif best == diagonal:
                traceback[i][j] = "DIAGONAL"
            elif best == up:
                traceback[i][j] = "UP"
            else:
                traceback[i][j] = "LEFT"

            if best > best_score:
                best_score = best
                best_position = (i, j)

    i, j = best_position
    end1, end2 = i, j

    aligned1 = []
    aligned2 = []

    while i > 0 and j > 0 and matrix[i][j] > 0:
        direction = traceback[i][j]

        if direction == "DIAGONAL":
            aligned1.append(sequence1[i - 1])
            aligned2.append(sequence2[j - 1])
            i -= 1
            j -= 1
        elif direction == "UP":
            aligned1.append(sequence1[i - 1])
            aligned2.append("-")
            i -= 1
        elif direction == "LEFT":
            aligned1.append("-")
            aligned2.append(sequence2[j - 1])
            j -= 1
        else:
            break

    return AlignmentResult(
        score=best_score,
        aligned_sequence1="".join(reversed(aligned1)),
        aligned_sequence2="".join(reversed(aligned2)),
        start1=i,
        end1=end1,
        start2=j,
        end2=end2,
    )
