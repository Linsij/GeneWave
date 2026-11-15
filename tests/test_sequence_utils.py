
import pytest

from genewave.sequence_utils import reverse_complement


def test_reverse_complement():
    assert reverse_complement("ATGC") == "GCAT"


def test_reverse_complement_with_unknown_base():
    assert reverse_complement("ATNG") == "CNAT"


def test_reverse_complement_lowercase():
    assert reverse_complement("atgc") == "GCAT"


def test_reverse_complement_invalid_sequence():
    with pytest.raises(ValueError):
        reverse_complement("ATGX")


def test_reverse_complement_empty_sequence():
    with pytest.raises(ValueError):
        reverse_complement("")
