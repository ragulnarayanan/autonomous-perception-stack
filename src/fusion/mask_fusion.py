# src/fusion/mask_fusion.py

import cv2
import numpy as np


def fuse_masks_with_lidar(
    detections,
    u,
    v,
    points_cam,
    image_shape
):

    fused_objects = []

    H, W = image_shape[:2]

    for det in detections:

        if det["mask"] is None:
            continue

        mask = cv2.resize(
            det["mask"].astype(np.uint8),
            (W, H),
            interpolation=cv2.INTER_NEAREST
        )

        point_indices = []

        for idx in range(len(u)):

            x = int(u[idx])
            y = int(v[idx])

            if (
                x < 0
                or x >= W
                or y < 0
                or y >= H
            ):
                continue

            if mask[y, x] > 0:
                point_indices.append(idx)

        if len(point_indices) == 0:
            continue

        object_points = points_cam[
            :3,
            point_indices
        ]

        fused_objects.append(
            {
                "class": det["class"],
                "confidence": det["confidence"],
                "mask": mask,
                "u": u[point_indices],
                "v": v[point_indices],
                "points": object_points,
                "num_points": len(point_indices)
            }
        )

    return fused_objects