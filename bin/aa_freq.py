#Calculates amino acid frequencies from an input file.

import sys
from collections import Counter

def read_fasta(fasta):
    """Reads FASTA sequences from stdin"""
    sequences = []
    with open(fasta, 'r') as file:
        for line in file:
            if not line.startswith('>'):
                sequences.append(line.strip())
    return sequences

def calculate_amino_acid_frequencies(sequences):
    """Calculates the frequencies of amino acids in the given sequence."""
    concatenated = ''.join(sequences)
    return Counter(concatenated)

def main():
    sequences = read_fasta(sys.argv[1])
    frequencies = calculate_amino_acid_frequencies(sequences)

    # Amino acids in the specified order
    amino_acids = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I',
                   'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']

    for aa in amino_acids:
        print(f"{frequencies[aa]}")

if __name__ == "__main__":
    main()
