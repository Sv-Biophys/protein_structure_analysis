def pdb_to_sequence_position(pdb_residue_number, offset=4):
    """Convert PDB residue numbering to sequence position."""

    return pdb_residue_number - offset


def convert_tm_regions(tm_regions, offset=4):
    """Convert TM regions from PDB numbering to sequence numbering."""

    converted = []

    for start, end in tm_regions:
        sequence_start = pdb_to_sequence_position(start, offset)
        sequence_end = pdb_to_sequence_position(end, offset)

        converted.append((sequence_start, sequence_end))

    return converted

def calculate_overlap(predicted_region, experimental_region):
    """Calculate the fraction of the experimental region covered by prediction."""

    predicted_start, predicted_end = predicted_region
    experimental_start, experimental_end = experimental_region

    overlap_start = max(predicted_start, experimental_start)
    overlap_end = min(predicted_end, experimental_end)

    if overlap_start > overlap_end:
        return 0.0

    overlap_length = overlap_end - overlap_start + 1
    experimental_length = experimental_end - experimental_start + 1

    return overlap_length / experimental_length

def find_tm_candidates(
    positions,
    profile,
    window_size=21,
    threshold=1.2
):
    """
    Find hydrophobic regions using a sliding window.

    Parameters
    ----------
    positions : list
        Sequence positions corresponding to the hydrophobicity profile.
    profile : list
        Hydrophobicity values.
    window_size : int
        Size of the sliding window.
    threshold : float
        Minimum average hydrophobicity.

    Returns
    -------
    list of tuples
        Predicted TM regions.
    """

    candidates = []

    for i in range(len(profile) - window_size + 1):

        window = profile[i:i + window_size]

        average_hydrophobicity = sum(window) / window_size

        if average_hydrophobicity >= threshold:

            start = positions[i]
            end = positions[i + window_size - 1]

            candidates.append(
                (start, end, average_hydrophobicity)
            )

    return candidates

def merge_overlapping_regions(candidates):
    """
    Merge overlapping hydrophobic regions.

    Parameters
    ----------
    candidates : list of tuples
        Regions represented as (start, end, score).

    Returns
    -------
    list of tuples
        Merged regions represented as (start, end, best_score).
    """

    if not candidates:
        return []

    candidates = sorted(candidates, key=lambda x: x[0])

    merged = []

    current_start, current_end, current_score = candidates[0]

    for start, end, score in candidates[1:]:

        if start <= current_end + 1:

            current_end = max(current_end, end)
            current_score = max(current_score, score)

        else:

            merged.append(
                (current_start, current_end, current_score)
            )

            current_start = start
            current_end = end
            current_score = score

    merged.append(
        (current_start, current_end, current_score)
    )

    return merged

def find_hydrophobic_peaks(positions, profile, min_score=1.2):
    """
    Find local maxima in a hydrophobicity profile.
    """

    peaks = []

    for i in range(1, len(profile) - 1):

        if (
            profile[i] > profile[i - 1]
            and profile[i] >= profile[i + 1]
            and profile[i] >= min_score
        ):
            peaks.append(
                (positions[i], profile[i])
            )

    return peaks

def select_tm_peaks(peaks, min_distance=20):
    """
    Select strongest hydrophobic peaks separated by a minimum distance.
    """

    sorted_peaks = sorted(
        peaks,
        key=lambda x: x[1],
        reverse=True
    )

    selected = []

    for position, score in sorted_peaks:

        too_close = False

        for selected_position, _ in selected:
            if abs(position - selected_position) < min_distance:
                too_close = True
                break

        if not too_close:
            selected.append((position, score))

    return sorted(selected)