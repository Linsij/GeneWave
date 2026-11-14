from pathlib import Path
from Bio import SeqIO


VALID_DNA_BASES = set("ACGTN")


def validate_dna_sequence(sequence: str) -> bool:
    """Validate a DNA sequence containing A, C, G, T, or N."""
    cleaned_sequence = str(sequence).upper()

    if not cleaned_sequence:
        raise ValueError("DNA sequence cannot be empty.")

    invalid_bases = set(cleaned_sequence) - VALID_DNA_BASES

    if invalid_bases:
        raise ValueError(
            f"Invalid DNA bases found: {', '.join(sorted(invalid_bases))}"
        )

    return True


def parse_fasta(file_path: str | Path):
    """Parse a FASTA file and validate every DNA sequence."""
    file_path = Path(file_path)

    if not file_path.is_file():
        raise FileNotFoundError(f"FASTA file not found: {file_path}")

    records = list(SeqIO.parse(file_path, "fasta"))

    if not records:
        raise ValueError("FASTA file contains no sequences.")

    for record in records:
        validate_dna_sequence(record.seq)

    return records
