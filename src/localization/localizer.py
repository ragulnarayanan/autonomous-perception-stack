# src/localization/localizer.py

import numpy as np


def compute_centroid(points):
    """
    points shape:
    (3, N)
    """

    return np.mean(
        points,
        axis=1
    )


def compute_distance(
    centroid
):

    return float(
        np.linalg.norm(
            centroid
        )
    )


def localize_object(
    obj
):
    points = obj.get(
        "points_lidar"
    )

    if points is None:
        points = obj.get(
            "points_cam"
        )

    if points is None:
        points = obj["points"]

    centroid = compute_centroid(
        points
    )

    distance = compute_distance(
        centroid
    )

    return {
        **obj,

        "centroid": centroid,

        "distance": distance
    }
