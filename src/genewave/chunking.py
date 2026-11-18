from .fasta import validate_dna_sequence


def chunk_sequence(sequence: str, chunk_size: int = 1000) -> list[str]:
    """Split a validated DNA sequence into fixed-size chunks."""
    validate_dna_sequence(sequence)

    if not isinstance(chunk_size, int) or isinstance(chunk_size, bool):
        raise TypeError("Chunk size must be an integer.")

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    sequence = sequence.upper()

    return [
        sequence[index:index + chunk_size]
        for index in range(0, len(sequence), chunk_size)
    ]
