# src/tracking/association.py

import numpy as np


def compute_distance_matrix(
    objects,
    tracks
):
    """
    Create distance matrix between
    current detections and existing tracks.
    """

    distance_matrix = []

    for obj in objects:

        row = []

        obj_centroid = obj["centroid"]

        for track in tracks:

            track_centroid = (
                track["centroid"]
            )

            dist = np.linalg.norm(
                obj_centroid -
                track_centroid
            )

            row.append(
                float(dist)
            )

        distance_matrix.append(
            row
        )

    return distance_matrix


def associate_tracks(
    objects,
    tracks,
    threshold=5.0,
    class_aware=True
):
    """
    Simple nearest-neighbor association.
    """

    matches = []

    used_tracks = set()

    for obj_idx, obj in enumerate(
        objects
    ):

        best_track = None

        best_distance = float(
            "inf"
        )

        for track_idx, track in enumerate(
            tracks
        ):

            if track_idx in used_tracks:
                continue

            if (
                class_aware
                and obj.get("class") != track.get("class")
            ):
                continue

            dist = np.linalg.norm(
                obj["centroid"]
                -
                track["centroid"]
            )

            if (
                dist < threshold
                and
                dist < best_distance
            ):

                best_distance = dist

                best_track = track_idx

        if best_track is not None:

            matches.append(
                (
                    obj_idx,
                    best_track
                )
            )

            used_tracks.add(
                best_track
            )

    return matches
