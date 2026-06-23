# src/fusion/object_statistics.py

from collections import Counter


def generate_scene_statistics(
    objects
):

    class_counts = Counter()

    distances = []

    for obj in objects:

        class_counts[
            obj["class"]
        ] += 1

        distances.append(
            obj["distance"]
        )

    nearest_distance = None

    if distances:
        nearest_distance = min(
            distances
        )

    return {
        "object_counts":
        dict(class_counts),

        "total_objects":
        len(objects),

        "nearest_object_distance":
        nearest_distance
    }