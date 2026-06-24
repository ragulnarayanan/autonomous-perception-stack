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
    min_points=10,
    max_length=8.0,
    min_width=0.5,
    min_height=0.5
):
    """
    Find likely fusion errors.
    """

    return [
        obj
        for obj in objects
        if is_suspicious_object(
            obj,
            max_height=max_height,
            min_points=min_points,
            max_length=max_length,
            min_width=min_width,
            min_height=min_height
        )
    ]


def is_suspicious_object(
    obj,
    max_height=5.0,
    min_points=10,
    max_length=8.0,
    min_width=0.5,
    min_height=0.5
):
    dims = obj["dimensions"]

    return (
        dims["height"] > max_height
        or
        dims["height"] < min_height
        or
        dims["length"] > max_length
        or
        dims["width"] < min_width
        or
        obj["num_points"] < min_points
    )


def filter_valid_objects(
    objects,
    **kwargs
):
    return [
        obj
        for obj in objects
        if not is_suspicious_object(
            obj,
            **kwargs
        )
    ]
