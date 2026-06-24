# src/bev/coordinate_conversion.py


def lidar_to_bev(
    centroid
):
    """
    Raw nuScenes LIDAR_TOP frame used by this project:

    X = left/right
    Y = forward
    Z = up/down

    BEV:

    X = forward
    Y = lateral
    """

    bev_x = float(
        centroid[1]
    )

    bev_y = float(
        centroid[0]
    )

    return bev_x, bev_y


def lidar_to_bev_plot(
    centroid
):
    """
    Plot-friendly BEV coordinates.

    X-axis = lateral position
    Y-axis = forward distance
    """

    lateral = float(
        centroid[0]
    )

    forward = float(
        centroid[1]
    )

    return lateral, forward


def camera_to_bev(
    centroid
):
    """
    Legacy camera-frame conversion.

    Camera frame:
    X = left/right, Y = vertical, Z = forward.
    """

    return (
        float(centroid[2]),
        float(centroid[0])
    )
