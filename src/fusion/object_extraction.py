# src/fusion/object_extraction.py

import numpy as np


def compute_object_centroid(
    points
):

    return np.mean(
        points,
        axis=1
    )


def compute_distance(
    centroid
):

    return np.linalg.norm(
        centroid
    )


def extract_object_properties(
    fused_objects
):

    extracted_objects = []

    for obj in fused_objects:

        centroid = (
            compute_object_centroid(
                obj["points"]
            )
        )

        distance = (
            compute_distance(
                centroid
            )
        )

        extracted_objects.append(
            {
                **obj,
                "centroid": centroid,
                "distance": float(
                    distance
                )
            }
        )

    return extracted_objects