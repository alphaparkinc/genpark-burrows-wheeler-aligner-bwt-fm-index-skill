"""Example demonstrating FM-Index genomic pattern search."""
from client import FMIndex

def main():
    genome = "ACGTACGTGACGTAGCTAGC"
    fm = FMIndex(genome)
    for q in ["ACGT", "TAGC", "AAAA"]:
        print(f"Occurrences of '{q}': {fm.count(q)}")

if __name__ == "__main__":
    main()
