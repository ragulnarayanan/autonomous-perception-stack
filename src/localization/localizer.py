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

    centroid = compute_centroid(
        obj["points"]
    )

    distance = compute_distance(
        centroid
    )

    return {
        **obj,

        "centroid": centroid,

        "distance": distance
    }