from pipeline.perception_pipeline import (
    run_perception_pipeline
)

from geometry.calibration import (
    get_camera_calibration,
    get_lidar_calibration
)

from geometry.lidar_projection_pipeline import (
    run_lidar_projection_pipeline
)

from fusion.mask_fusion import (
    fuse_masks_with_lidar
)

from fusion.object_extraction import (
    extract_object_properties
)


def run_fusion_pipeline(
    nusc,
    image,
    cam_data,
    lidar_data
):
    """
    Complete Camera-LiDAR Fusion Pipeline

    Returns
    -------
    dict
    """

    # --------------------------------
    # Perception
    # --------------------------------

    detections = (
        run_perception_pipeline(
            image
        )
    )

    # --------------------------------
    # Calibration
    # --------------------------------

    cam_calib = (
        get_camera_calibration(
            nusc,
            cam_data
        )
    )

    lidar_calib = (
        get_lidar_calibration(
            nusc,
            lidar_data
        )
    )

    # --------------------------------
    # Projection
    # --------------------------------

    u, v, points_cam, pc = (
        run_lidar_projection_pipeline(
            nusc,
            lidar_data,
            lidar_calib,
            cam_calib
        )
    )

    # --------------------------------
    # Original LiDAR XYZ
    # --------------------------------

    points_lidar = (
        pc.points[:3, :]
    )

    # --------------------------------
    # Fusion
    # --------------------------------

    fused_objects = (
        fuse_masks_with_lidar(
            detections,
            u,
            v,
            points_cam,
            points_lidar,
            image.shape
        )
    )

    # --------------------------------
    # Object State Estimation
    # --------------------------------

    objects = (
        extract_object_properties(
            fused_objects
        )
    )

    # --------------------------------
    # Return Everything
    # --------------------------------

    return {
        "detections": detections,

        "u": u,
        "v": v,

        "points_cam": points_cam,

        "points_lidar": points_lidar,

        "pointcloud": pc,

        "fused_objects": fused_objects,

        "objects": objects
    }