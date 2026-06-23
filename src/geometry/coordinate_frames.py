import numpy as np

from geometry.transforms import (
    build_transform_matrix,
    invert_transform,
    apply_transform
)


def lidar_to_camera(
    points_hom,
    lidar_calib,
    cam_calib
):
    """
    Transform LiDAR points to camera frame.

    LiDAR
      ↓
    Ego
      ↓
    Camera
    """

    T_lidar_ego = build_transform_matrix(
        lidar_calib["translation"],
        lidar_calib["rotation"]
    )

    T_cam_ego = build_transform_matrix(
        cam_calib["translation"],
        cam_calib["rotation"]
    )

    T_ego_cam = invert_transform(T_cam_ego)

    points_ego = apply_transform(
        points_hom,
        T_lidar_ego
    )

    points_cam = apply_transform(
        points_ego,
        T_ego_cam
    )

    return points_cam