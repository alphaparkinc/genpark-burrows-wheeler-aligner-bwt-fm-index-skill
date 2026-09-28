"""Ferragina-Manzini (FM) Index for Genomic Search.
100% Python Standard Library.
"""

class FMIndex:
    """Exact substring count and search using BWT and Occ tables."""
    def __init__(self, text):
        self.text = text + "$"
        self.bwt, self.suffix_array = self._build_bwt(self.text)
        self.C, self.Occ = self._build_counts_and_occ(self.bwt)

    def _build_bwt(self, text):
        suffixes = sorted(range(len(text)), key=lambda i: text[i:])
        bwt = "".join(text[i - 1] for i in suffixes)
        return bwt, suffixes

    def _build_counts_and_occ(self, bwt):
        chars = sorted(set(bwt))
        counts = {c: bwt.count(c) for c in chars}
        C = {}
        total = 0
        for c in chars:
            C[c] = total
            total += counts[c]
            
        Occ = {c: [0] * (len(bwt) + 1) for c in chars}
        for i, ch in enumerate(bwt):
            for c in chars:
                Occ[c][i + 1] = Occ[c][i] + (1 if ch == c else 0)
        return C, Occ

    def count(self, pattern):
        """Returns the number of occurrences of pattern in indexed text."""
        l = 0
        r = len(self.bwt) - 1
        for ch in reversed(pattern):
            if ch not in self.C:
                return 0
            l = self.C[ch] + self.Occ[ch][l]
            r = self.C[ch] + self.Occ[ch][r + 1] - 1
            if l > r:
                return 0
        return r - l + 1
