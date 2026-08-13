def find_motif(residues, motif):
    """
    Ищет аминокислотный мотив в белке.
    """
    motif = motif.upper()
    
    if not motif:
        return []

    sequence = ""

    for residue in residues:
        sequence += residue["one_letter"]

    matches = []

    for i in range(len(sequence) - len(motif) + 1):
        fragment = sequence[i:i + len(motif)]
        if fragment == motif:
            matches.append({
                "start": i + 1,
                "end": i + len(motif),
                "sequence": fragment
            })

    return matches