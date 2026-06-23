def get_camera_calibration(nusc, cam_data):

    return nusc.get(
        "calibrated_sensor",
        cam_data["calibrated_sensor_token"]
    )


def get_lidar_calibration(nusc, lidar_data):

    return nusc.get(
        "calibrated_sensor",
        lidar_data["calibrated_sensor_token"]
    )


def get_camera_intrinsic(cam_calib):

    return cam_calib["camera_intrinsic"]


def get_camera_ego_pose(nusc, cam_data):

    return nusc.get(
        "ego_pose",
        cam_data["ego_pose_token"]
    )


def get_lidar_ego_pose(nusc, lidar_data):

    return nusc.get(
        "ego_pose",
        lidar_data["ego_pose_token"]
    )