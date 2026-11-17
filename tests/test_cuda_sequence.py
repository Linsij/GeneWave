import pytest
from numba import cuda

from genewave.cuda_utils import cuda_reverse_complement
from genewave.sequence_utils import reverse_complement


pytestmark = pytest.mark.skipif(
    not cuda.is_available(),
    reason="CUDA GPU is not available",
)


@pytest.mark.parametrize(
    "sequence",
    [
        "ATGC",
        "ATNG",
        "atgc",
        "AACCGGTT",
        "A" * 1000,
    ],
)
def test_cuda_reverse_complement(sequence):
    expected = reverse_complement(sequence)
    assert cuda_reverse_complement(sequence) == expected


def test_cuda_reverse_complement_invalid_sequence():
    with pytest.raises(ValueError):
        cuda_reverse_complement("ATGX")
