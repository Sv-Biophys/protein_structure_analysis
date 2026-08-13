def helix_center(start, end):
    """Возвращает центральную позицию α-спирали."""
    return (start + end) / 2


def distance_to_helix(peak_position, helix):
    """Считает расстояние от пика до центра α-спирали."""
    start, end = helix

    center = helix_center(start, end)

    return abs(peak_position - center)

def match_peaks_to_helices(peaks, helices):
    """
    Сопоставляет каждый предсказанный пик
    с ближайшей экспериментальной α-спиралью.
    """

    matches = []

    for peak_position, score in peaks:
        best_helix = None
        best_distance = float("inf")

        for helix in helices:
            distance = distance_to_helix(peak_position, helix)

            if distance < best_distance:
                best_distance = distance
                best_helix = helix

        matches.append({
            "peak": peak_position,
            "score": score,
            "helix": best_helix,
            "distance": best_distance
        })

    return matches

def calculate_validation_statistics(matches):
    """
    Рассчитывает статистику качества предсказания.
    """

    distances = [
        match["distance"]
        for match in matches
    ]

    mean_error = sum(distances) / len(distances)

    return {
        "mean_error": mean_error,
        "max_error": max(distances),
        "min_error": min(distances),
    }
def is_peak_inside_helix(peak_position, helix):
    """
    Проверяет, находится ли предсказанный пик
    внутри экспериментальной α-спирали.
    """

    start, end = helix

    return start <= peak_position <= end

def calculate_overlap_statistics(matches):
    """
    Рассчитывает, сколько предсказанных пиков
    попало внутрь экспериментальных α-спиралей.
    """

    total = len(matches)

    inside = sum(
        is_peak_inside_helix(
            match["peak"],
            match["helix"]
        )
        for match in matches
    )

    accuracy = inside / total if total > 0 else 0

    return {
        "total_peaks": total,
        "peaks_inside_helices": inside,
        "accuracy": accuracy,
    }