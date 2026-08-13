from Bio.PDB import PPBuilder
from Bio.SeqUtils import molecular_weight
from collections import Counter
from src.utils.download_pdb import download_pdb
from src.analysis.residue_analysis import extract_residues
from src.analysis.motif_search import find_motif

from Bio.PDB import PDBParser

def load_structure(pdb_file: str):
    """
    Загружает PDB-структуру.
    """

    parser = PDBParser(QUIET=True)

    structure = parser.get_structure(
        "protein",
        pdb_file
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

    residues = extract_residues(structure)

    motif = input("Введите мотив (например RGD): ").upper()
    matches = find_motif(residues, motif)
    if matches:
        print(f"\nНайдено совпадений: {len(matches)}")

        for match in matches:
            print(
                f"{match['sequence']} "
                f"(позиции {match['start']}-{match['end']})"
            )
    else:
        print("\nМотив не найден.")

    report = structure_info(structure)

    save_report(report, "results/report.txt")

    print("Анализ завершён.")

if __name__ == "__main__":
    main()