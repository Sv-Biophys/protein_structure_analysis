import matplotlib.pyplot as plt


KYTE_DOOLITTLE = {
    "A": 1.8,
    "R": -4.5,
    "N": -3.5,
    "D": -3.5,
    "C": 2.5,
    "Q": -3.5,
    "E": -3.5,
    "G": -0.4,
    "H": -3.2,
    "I": 4.5,
    "L": 3.8,
    "K": -3.9,
    "M": 1.9,
    "F": 2.8,
    "P": -1.6,
    "S": -0.8,
    "T": -0.7,
    "W": -0.9,
    "Y": -1.3,
    "V": 4.2,
}


def calculate_hydrophobicity(sequence):
    """Calculate Kyte-Doolittle hydrophobicity for each residue."""

    hydrophobicity = []

    for residue in sequence:
        value = KYTE_DOOLITTLE.get(residue)

        if value is None:
            raise ValueError(f"Unknown amino acid: {residue}")

        hydrophobicity.append(value)

    return hydrophobicity


def calculate_hydrophobicity_profile(sequence, window_size=19):
    """Calculate a sliding-window Kyte-Doolittle hydrophobicity profile."""

    values = calculate_hydrophobicity(sequence)

    if window_size > len(values):
        raise ValueError(
            "Window size cannot be larger than sequence length."
        )

    positions = []
    profile = []

    for i in range(len(values) - window_size + 1):
        window = values[i:i + window_size]
        average = sum(window) / window_size

        center = i + window_size // 2 + 1

        positions.append(center)
        profile.append(average)

    return positions, profile


def get_sequence_from_structure(structure):
    """Extract the protein sequence from the first chain of a structure."""

    from Bio.PDB import PPBuilder

    ppb = PPBuilder()

    for model in structure:
        for chain in model:
            sequence = ""

            for peptide in ppb.build_peptides(chain):
                sequence += str(peptide.get_sequence())

            if sequence:
                return sequence

    raise ValueError("No protein sequence found in structure.")


def find_hydrophobic_regions(
    positions,
    profile,
    threshold=1.6,
    min_length=15
):
    """Find continuous hydrophobic regions."""

    regions = []
    start = None

    for position, value in zip(positions, profile):

        if value >= threshold and start is None:
            start = position

        elif value < threshold and start is not None:
            end = position - 1

            if end - start + 1 >= min_length:
                regions.append((start, end))

            start = None

    if start is not None:
        end = positions[-1]

        if end - start + 1 >= min_length:
            regions.append((start, end))

    return regions


def plot_hydrophobicity(positions, profile, output_file):
    """Plot and save a hydrophobicity profile."""

    plt.figure(figsize=(10, 5))

    plt.plot(positions, profile)

    plt.axhline(
        y=1.6,
        linestyle="--",
        label="Hydrophobicity threshold"
    )

    plt.xlabel("Residue position")
    plt.ylabel("Kyte-Doolittle hydrophobicity")
    plt.title("Hydrophobicity profile")
    plt.legend()

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()