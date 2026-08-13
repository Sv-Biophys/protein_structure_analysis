from Bio.PDB.Polypeptide import is_aa
from Bio.SeqUtils import seq1


def extract_residues(structure):
    """
    Извлекает информацию обо всех аминокислотных остатках.
    """

    residues = []

    for model in structure:
        for chain in model:
            for residue in chain:

                if not is_aa(residue, standard=True):
                    continue

                residue_info = {
                    "chain": chain.id,
                    "number": residue.id[1],
                    "name": residue.get_resname(),
                    "one_letter": seq1(residue.get_resname())
                }

                residues.append(residue_info)

    return residues