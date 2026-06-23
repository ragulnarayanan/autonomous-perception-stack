import pandas as pd
import numpy as np


def create_fusion_summary(
    objects
):
    """
    Create validation dataframe.
    """

    rows = []

    for obj in objects:

        dimensions = obj.get(
            "dimensions",
            {}
        )

        rows.append(
            {
                "class":
                obj["class"],

                "confidence":
                round(
                    obj["confidence"],
                    3
                ),

                "distance":
                round(
                    obj["distance"],
                    2
                ),

                "num_points":
                obj["num_points"],

                "length":
                round(
                    dimensions.get(
                        "length",
                        0
                    ),
                    2
                ),

                "width":
                round(
                    dimensions.get(
                        "width",
                        0
                    ),
                    2
                ),

                "height":
                round(
                    dimensions.get(
                        "height",
                        0
                    ),
                    2
                )
            }
        )

    return pd.DataFrame(
        rows
    )


def filter_sparse_objects(
    objects,
    min_points=20
):

    return [
        obj
        for obj in objects
        if obj["num_points"] >= min_points
    ]


def inspect_height_distribution(
    obj
):
    """
    Inspect LiDAR Z values.
    """

    z = obj["points_lidar"][2]

    return {
        "min_z":
        float(
            np.min(z)
        ),

        "max_z":
        float(
            np.max(z)
        ),

        "height":
        float(
            np.max(z)
            -
            np.min(z)
        )
    }


def find_suspicious_objects(
    objects,
    max_height=5.0,
    min_points=20
):
    """
    Find likely fusion errors.
    """

    suspicious = []

    for obj in objects:

        dims = obj["dimensions"]

        if (
            dims["height"] > max_height
            or
            obj["num_points"] < min_points
        ):

            suspicious.append(
                obj
            )

    return suspicious