import pytest

from src.genewave.fasta import parse_fasta, validate_dna_sequence


def test_valid_dna_sequence():
    assert validate_dna_sequence("ATGC") is True


def test_valid_dna_with_unknown_bases():
    assert validate_dna_sequence("ATGNNN") is True


def test_invalid_dna_sequence():
    with pytest.raises(ValueError, match="Invalid DNA bases"):
        validate_dna_sequence("ATGX")


def test_empty_dna_sequence():
    with pytest.raises(ValueError, match="cannot be empty"):
        validate_dna_sequence("")


def test_parse_sample_fasta():
    records = parse_fasta("data/raw/sample_genome.fasta")
    assert len(records) == 3
    assert records[0].id == "gene_001"


def test_missing_fasta_file():
    with pytest.raises(FileNotFoundError):
        parse_fasta("data/raw/missing.fasta")
