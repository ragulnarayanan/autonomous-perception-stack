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
    Object dimensions from LiDAR points.

    X = forward
    Y = left/right
    Z = up/down

    Length and width are computed in an object-aligned
    ground-plane frame, not directly from raw LiDAR X/Y axes.
    """

    z = points[2]

    xy = points[:2].T
    xy_centered = (
        xy
        -
        np.mean(
            xy,
            axis=0
        )
    )

    if points.shape[1] >= 2:
        covariance = np.cov(
            xy_centered,
            rowvar=False
        )

        eigenvalues, eigenvectors = np.linalg.eigh(
            covariance
        )

        order = np.argsort(
            eigenvalues
        )[::-1]

        axes = eigenvectors[
            :,
            order
        ]

        footprint = xy_centered @ axes
    else:
        footprint = xy_centered

    major_axis = footprint[:, 0]
    minor_axis = footprint[:, 1]

    return {
        "length": float(
            np.max(major_axis)
            -
            np.min(major_axis)
        ),
        "width": float(
            np.max(minor_axis)
            -
            np.min(minor_axis)
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
