import os
import numpy as np

from nuscenes.utils.data_classes import LidarPointCloud

from geometry.coordinate_frames import lidar_to_camera
from geometry.projection import project_points_to_image


def load_lidar_pointcloud(nusc, lidar_data):
    """
    Load LiDAR point cloud from nuScenes.
    """

    lidar_path = os.path.join(
        nusc.dataroot,
        lidar_data["filename"]
    )

    pc = LidarPointCloud.from_file(
        lidar_path
    )

    return pc


def convert_to_homogeneous(points):
    """
    Convert (3,N) -> (4,N)
    """

    ones = np.ones(
        (1, points.shape[1])
    )

    return np.vstack([points, ones])


def run_lidar_projection_pipeline(
    nusc,
    lidar_data,
    lidar_calib,
    cam_calib
):
    """
    Complete Week 2 pipeline.

    Returns:
        u, v
        points_cam
        point_cloud
    """

    # Load point cloud
    pc = load_lidar_pointcloud(
        nusc,
        lidar_data
    )

    # XYZ only
    points = pc.points[:3, :]

    # Homogeneous coordinates
    points_hom = convert_to_homogeneous(
        points
    )

    # LiDAR -> Camera
    points_cam = lidar_to_camera(
        points_hom,
        lidar_calib,
        cam_calib
    )

    # Camera -> Image
    u, v, valid_mask = project_points_to_image(
        points_cam,
        cam_calib["camera_intrinsic"],
        return_mask=True
    )

    points_cam = points_cam[
        :,
        valid_mask
    ]

    pc.points = pc.points[
        :,
        valid_mask
    ]

    return (
        u,
        v,
        points_cam,
        pc
    )
