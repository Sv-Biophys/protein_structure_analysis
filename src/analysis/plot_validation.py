import matplotlib.pyplot as plt

from src.analysis.structure_analysis import load_structure
from src.analysis.hydrophobicity import (
    get_sequence_from_structure,
    calculate_hydrophobicity_profile,
)
from src.analysis.tm_analysis import find_hydrophobic_peaks, select_tm_peaks
from src.analysis.secondary_structure import get_experimental_helices
from src.analysis.validation import (
    match_peaks_to_helices,
    calculate_validation_statistics,
    calculate_overlap_statistics,
)


def main():
    structure = load_structure("data/pdb/1c3w.pdb")
    sequence = get_sequence_from_structure(structure)

    positions, profile = calculate_hydrophobicity_profile(sequence)

    peaks = find_hydrophobic_peaks(positions, profile)
    selected_peaks = select_tm_peaks(peaks, min_distance=20)

    helices = get_experimental_helices()

    matches = match_peaks_to_helices(
        selected_peaks,
        helices,
    )

    validation_stats = calculate_validation_statistics(matches)
    overlap_stats = calculate_overlap_statistics(matches)

    print("Validation results")
    print("------------------")
    print(f"Matched peaks: {overlap_stats['peaks_inside_helices']} / {overlap_stats['total_peaks']}")
    print(f"Accuracy: {overlap_stats['accuracy']:.2f}")
    print(f"Mean distance: {validation_stats['mean_error']:.2f} residues")
    print(f"Maximum distance: {validation_stats['max_error']:.2f} residues")
    print(f"Minimum distance: {validation_stats['min_error']:.2f} residues")

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        positions,
        profile,
        linewidth=2,
        label="Hydrophobicity profile",
    )

    peak_positions = [position for position, score in selected_peaks]
    peak_scores = [score for position, score in selected_peaks]

    ax.scatter(
        peak_positions,
        peak_scores,
        s=60,
        zorder=3,
        label="Predicted TM peaks",
    )

    for start, end in helices:
        ax.axvspan(
            start,
            end,
            alpha=0.15,
        )

    ax.set_xlabel("Residue position")
    ax.set_ylabel("Hydrophobicity")
    ax.set_title("Hydrophobicity Profile and Structural Validation")

    ax.legend()
    ax.grid(alpha=0.2)

    plt.tight_layout()

    plt.savefig(
        "results/hydrophobicity_validation.png",
        dpi=300,
    )

    plt.close()


if __name__ == "__main__":
    main()