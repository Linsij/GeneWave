
from .fasta import validate_dna_sequence


def reverse_complement(sequence: str) -> str:
    """Return the reverse complement of a DNA sequence."""
    validate_dna_sequence(sequence)

    sequence = str(sequence).upper()
    complement = str.maketrans("ACGTN", "TGCAN")

    return sequence.translate(complement)[::-1]
