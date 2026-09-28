# FM-Index Genomic Sequence Aligner Skill

Ferragina-Manzini (FM) index implementation leveraging the Burrows-Wheeler Transform for sublinear genomic pattern searching.

```mermaid
flowchart LR
    Genome["Reference Genome String"] --> Suffix["Suffix Array"]
    Suffix --> BWT["BWT String Transformation"]
    BWT --> Occ["Occ Occurrence Table & C Count Array"]
    Pattern["Query Pattern (e.g. ACGT)"] --> Backward["Backward Search (LF-Mapping)"]
    Occ --> Backward
    Backward --> Hits["Exact Occurrences Count & Range"]
```

## Features
- **100% Python Standard Library**: Pure suffix sorting and backward search logic.
- **Fast Backward Search**: Pattern matching proportional to query length \(O(m)\).
- **Exact Count Capabilities**: Instant frequency reporting across large references.
