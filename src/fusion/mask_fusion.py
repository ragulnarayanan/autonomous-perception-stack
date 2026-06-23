# src/fusion/mask_fusion.py

import cv2
import numpy as np
from fusion.cluster_filter import (
    largest_cluster
)

def fuse_masks_with_lidar(
    detections,
    u,
    v,
    points_cam,
    points_lidar,
    image_shape,
    min_points=20
):
    """
    Associate projected LiDAR points
    with YOLO segmentation masks.

    Improvements:
    -------------
    1. Higher-confidence objects claim points first
    2. Each LiDAR point belongs to only one object
    3. Remove sparse detections
    4. Basic height filtering
    """

    fused_objects = []

    H, W = image_shape[:2]
    u_values = np.asarray(u)
    v_values = np.asarray(v)

    # ----------------------------------
    # Highest confidence first
    # ----------------------------------

    detections = sorted(
        detections,
        key=lambda x: x["confidence"],
        reverse=True
    )

    # ----------------------------------
    # Point ownership tracking
    # ----------------------------------

    assigned_points = set()

    for det in detections:

        if det["mask"] is None:
            continue

        # ----------------------------------
        # Resize mask to image dimensions
        # ----------------------------------

        mask = cv2.resize(
            det["mask"].astype(np.uint8),
            (W, H),
            interpolation=cv2.INTER_NEAREST
        )

        point_indices = []

        # ----------------------------------
        # Find projected points inside mask
        # ----------------------------------

        for idx in range(len(u_values)):

            # Point already claimed
            if idx in assigned_points:
                continue

            x = int(u_values[idx])
            y = int(v_values[idx])

            if (
                x < 0
                or x >= W
                or y < 0
                or y >= H
            ):
                continue

            if mask[y, x] > 0:

                point_indices.append(idx)

        # ----------------------------------
        # Reject weak clusters
        # ----------------------------------

        if len(point_indices) < min_points:
            continue

        point_indices = np.asarray(
            point_indices,
            dtype=int
        )

        # ----------------------------------
        # Extract object point cloud
        # ----------------------------------

        object_points_cam = (
            points_cam[
                :3,
                point_indices
            ]
        )

        object_points_lidar = (
            points_lidar[
                :,
                point_indices
            ]
        )

        # ----------------------------------
        # Basic geometry cleanup
        #
        # Camera coordinates:
        # X = left/right
        # Y = up/down
        # Z = forward
        #
        # Remove extreme vertical outliers
        # ----------------------------------
        object_points_lidar, cluster_mask = (
            largest_cluster(
                object_points_lidar,
                eps=1.0,
                min_samples=10,
                return_mask=True
            )
        )

        object_points_cam = (
            object_points_cam[
                :,
                cluster_mask
            ]
        )

        object_point_indices = point_indices[cluster_mask]
        object_u = u_values[object_point_indices]
        object_v = v_values[object_point_indices]

        if object_points_lidar.shape[1] > 0:

            # LiDAR frame:
            # X = forward
            # Y = left/right
            # Z = up/down

            vertical_mask = (
                np.abs(
                    object_points_lidar[2]
                ) < 5.0
            )

            object_points_lidar = (
                object_points_lidar[
                    :,
                    vertical_mask
                ]
            )

            object_points_cam = (
                object_points_cam[
                    :,
                    vertical_mask
                ]
            )

            object_u = object_u[vertical_mask]
            object_v = object_v[vertical_mask]
            object_point_indices = object_point_indices[vertical_mask]

        if object_points_lidar.shape[1] < min_points:
            continue

        assigned_points.update(
            object_point_indices.tolist()
        )


        # ----------------------------------
        # Save fused object
        # ----------------------------------

        fused_objects.append(
            {

                "class":
                det["class"],

                "confidence":
                det["confidence"],

                "mask":
                mask,

                "u":
                object_u,

                "v":
                object_v,

                "points_cam":
                object_points_cam,

                "points_lidar":
                object_points_lidar,

                "num_points":
                object_points_lidar.shape[1]
            }
        )

    return fused_objects
