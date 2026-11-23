import pytest
from numba import cuda

from genewave.alignment import smith_waterman
from genewave.cuda_alignment import cuda_smith_waterman


pytestmark = pytest.mark.skipif(
    not cuda.is_available(),
    reason="CUDA GPU is not available",
)


@pytest.mark.parametrize(
    "sequence1, sequence2",
    [
        ("ACGT", "ACGT"),
        ("TTACGTAA", "ACGT"),
        ("AAAA", "TTTT"),
        ("ACGGT", "ACGT"),
        ("GATTACA", "GCATGCT"),
        ("AAAACCCCGGGG", "AAAATCCCCGGGG"),
        ("atgc", "ATGC"),
        ("A" * 100, "A" * 100),
    ],
)
def test_cuda_alignment_matches_cpu(sequence1, sequence2):
    cpu_result = smith_waterman(sequence1, sequence2)
    gpu_result = cuda_smith_waterman(sequence1, sequence2)

    assert gpu_result == cpu_result


def test_cuda_alignment_empty_sequence():
    with pytest.raises(ValueError, match="DNA sequence cannot be empty"):
        cuda_smith_waterman("", "ACGT")

def test_cuda_alignment_invalid_sequence():
    with pytest.raises(ValueError):
        cuda_smith_waterman("ATGX", "ACGT")


def test_cuda_alignment_invalid_match_score():
    with pytest.raises(ValueError):
        cuda_smith_waterman("ACGT", "ACGT", match_score=0)


def test_cuda_alignment_invalid_score_type():
    with pytest.raises(TypeError):
        cuda_smith_waterman("ACGT", "ACGT", match_score=2.5)