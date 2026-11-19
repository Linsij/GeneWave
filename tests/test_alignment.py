import pytest

from genewave.alignment import smith_waterman


def test_exact_match():
    result = smith_waterman("ACGT", "ACGT")

    assert result.score == 8
    assert result.aligned_sequence1 == "ACGT"
    assert result.aligned_sequence2 == "ACGT"


def test_partial_local_alignment():
    result = smith_waterman("TTACGTAA", "GGACGTCC")

    assert result.score == 8
    assert result.aligned_sequence1 == "ACGT"
    assert result.aligned_sequence2 == "ACGT"


def test_mismatch():
    result = smith_waterman("AAAA", "TTAA")

    assert result.score == 4
    assert result.aligned_sequence1 == "AA"
    assert result.aligned_sequence2 == "AA"


def test_alignment_with_gap():
    result = smith_waterman("ACGGT", "ACGT")

    assert result.score == 6
    assert len(result.aligned_sequence1) == len(result.aligned_sequence2)


def test_lowercase_sequences():
    result = smith_waterman("acgt", "ACGT")

    assert result.score == 8
    assert result.aligned_sequence1 == "ACGT"


def test_invalid_dna_sequence():
    with pytest.raises(ValueError):
        smith_waterman("ACGX", "ACGT")


def test_empty_sequence():
    with pytest.raises(ValueError):
        smith_waterman("", "ACGT")


def test_invalid_scoring_type():
    with pytest.raises(TypeError):
        smith_waterman("ACGT", "ACGT", match_score=2.5)


def test_invalid_match_score():
    with pytest.raises(ValueError):
        smith_waterman("ACGT", "ACGT", match_score=0)
