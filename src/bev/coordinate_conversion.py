# src/bev/coordinate_conversion.py


def camera_to_bev(
    centroid
):
    """
    Camera frame:

    X = left/right
    Y = vertical
    Z = forward

    BEV:

    X = forward
    Y = lateral
    """

    bev_x = float(
        centroid[2]
    )

    bev_y = float(
        centroid[0]
    )

    return bev_x, bev_y