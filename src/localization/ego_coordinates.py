# src/localization/ego_coordinates.py


def get_ego_position(
    centroid
):

    return {
        "x": float(
            centroid[0]
        ),

        "y": float(
            centroid[1]
        ),

        "z": float(
            centroid[2]
        )
    }