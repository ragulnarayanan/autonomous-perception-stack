import numpy as np


def project_points_to_image(
    points_cam,
    camera_intrinsic,
    return_mask=False
):
    """
    Project camera-frame points
    to image coordinates.
    """

    K = np.array(camera_intrinsic)

    valid_mask = points_cam[2, :] > 0

    points_cam = points_cam[:, valid_mask]

    proj = K @ points_cam[:3, :]

    u = proj[0] / proj[2]
    v = proj[1] / proj[2]

    if return_mask:
        return u, v, valid_mask

    return u, v
