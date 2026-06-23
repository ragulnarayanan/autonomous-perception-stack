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


def compute_dimensions(
    points
):
    """
    LiDAR frame dimensions.

    X = forward
    Y = left/right
    Z = up/down
    """

    x = points[0]
    y = points[1]
    z = points[2]

    return {
        "length": float(
            np.max(x) - np.min(x)
        ),
        "width": float(
            np.max(y) - np.min(y)
        ),
        "height": float(
            np.max(z) - np.min(z)
        )
    }


def extract_object_properties(
    fused_objects
):

    extracted_objects = []

    for obj in fused_objects:

        # --------------------------
        # Use LiDAR geometry
        # --------------------------

        points = obj["points_lidar"]

        if points.shape[1] == 0:
            continue

        centroid = (
            compute_object_centroid(
                points
            )
        )

        distance = (
            compute_distance(
                centroid
            )
        )

        dimensions = (
            compute_dimensions(
                points
            )
        )

        extracted_objects.append(
            {
                **obj,

                "centroid":
                centroid,

                "distance":
                float(distance),

                "position":
                {
                    "x": float(
                        centroid[0]
                    ),

                    "y": float(
                        centroid[1]
                    ),

                    "z": float(
                        centroid[2]
                    )
                },

                "dimensions":
                dimensions
            }
        )

    return extracted_objects