from Bio.PDB import PDBList
from Bio.PDB.Polypeptide import is_aa
from Bio.SeqUtils import seq1
from Bio.PDB import PPBuilder
from Bio.SeqUtils import molecular_weight
from collections import Counter

def download_pdb(pdb_id: str, output_dir: str = "data/pdb"):
    """
    Скачивает структуру белка из Protein Data Bank.
    """

    pdbl = PDBList()

    filename = pdbl.retrieve_pdb_file(
        pdb_id,
        pdir=output_dir,
        file_format="pdb"
    )

    return filename

from Bio.PDB import PDBParser

def load_structure(pdb_file: str):
    """
    Загружает PDB-структуру.
    """

    parser = PDBParser(QUIET=True)

    structure = parser.get_structure(
        id="protein",
        file=pdb_file
    )

    return structure


def structure_info(structure):
    """
    Выводит основную информацию о структуре.
    """
    ppb = PPBuilder()

    report = [] 

    models = list(structure)

    for model in models:
        chains = list(model)
        report.append(f"\n=== Модель {model.id} ===")
        report.append(f"Цепей: {len(chains)}")
  
        for chain in chains:

            sequence = ""

            for peptide in ppb.build_peptides(chain):
                sequence += str(peptide.get_sequence())

            mass = molecular_weight(sequence, seq_type="protein")
      

            residues = list(chain)
            atoms = list(chain.get_atoms())

            report.append(f"\nЦепь {chain.id}")
            report.append("-" * 30)
            report.append(f"Остатков: {len(residues)}")
            report.append(f"Атомов: {len(atoms)}")
            report.append(f"Длина последовательности: {len(sequence)} аминокислот")
            report.append(f"Молекулярная масса: {mass / 1000:.2f} kDa")
            report.append(f"Последовательность:")

            for i in range(0, len(sequence), 60):
                report.append(sequence[i:i + 60])

            amino_acid_counts = Counter(sequence)
            report.append("Аминокислотный состав:")
            for amino_acid, count in sorted(amino_acid_counts.items()):
                percent = count / len(sequence) * 100
                report.append(f"{amino_acid}: {count:3d} ({percent:5.1f}%)")

    
    return report
            

def save_report(report, filename):
    """Сохраняет отчет в текстовый файл."""

    with open(filename, "w") as file:
        file.write("\n".join(report))

def main():
    pdb_id = input("Enter PDB ID: ").upper()

    filename = download_pdb(pdb_id)

    print(f"Файл сохранён: {filename}")

    structure = load_structure(filename)

    report = structure_info(structure)

    save_report(report, "results/report.txt")

if __name__ == "__main__":
    main()