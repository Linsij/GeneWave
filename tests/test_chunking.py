import pytest

from genewave.chunking import chunk_sequence


def test_chunk_sequence():
    assert chunk_sequence("ATGCCGTA", 4) == ["ATGC", "CGTA"]


def test_chunk_sequence_with_remaining_bases():
    assert chunk_sequence("ATGCCGTAA", 4) == ["ATGC", "CGTA", "A"]


def test_chunk_sequence_lowercase():
    assert chunk_sequence("atgc", 2) == ["AT", "GC"]


def test_chunk_sequence_invalid_dna():
    with pytest.raises(ValueError):
        chunk_sequence("ATGX", 2)


def test_chunk_sequence_zero_size():
    with pytest.raises(ValueError):
        chunk_sequence("ATGC", 0)


def test_chunk_sequence_invalid_size_type():
    with pytest.raises(TypeError):
        chunk_sequence("ATGC", 2.5)


def test_chunk_sequence_empty_input():
    with pytest.raises(ValueError):
        chunk_sequence("", 2)
