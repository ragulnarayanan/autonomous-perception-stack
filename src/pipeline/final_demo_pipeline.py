# src/pipeline/final_demo_pipeline.py

import os

import cv2

from bev.scene_builder import (
    build_bev_scene
)
from bev.occupancy_grid import (
    create_grid
)
from bev.occupancy_mapper import (
    populate_grid
)
from fusion.validation import (
    filter_valid_objects,
    find_suspicious_objects
)
from perception.inference import (
    PerceptionPipeline
)
from pipeline.fusion_pipeline import (
    run_fusion_from_detections
)
from prediction.trajectory import (
    predict_all_tracks
)
from tracking.tracker import (
    ObjectTracker
)


def iter_scene_samples(
    nusc,
    scene_index=0,
    max_frames=3
):
    """
    Yield sample records from one nuScenes scene.
    """

    scene = nusc.scene[
        scene_index
    ]

    sample_token = scene[
        "first_sample_token"
    ]

    frame_index = 0

    while (
        sample_token
        and frame_index < max_frames
    ):

        sample = nusc.get(
            "sample",
            sample_token
        )

        yield frame_index, sample

        sample_token = sample[
            "next"
        ]

        frame_index += 1


def load_camera_image(
    nusc,
    cam_data
):
    """
    Load RGB camera image from a nuScenes sample_data record.
    """

    image_path = os.path.join(
        nusc.dataroot,
        cam_data["filename"]
    )

    image = cv2.imread(
        image_path
    )

    if image is None:
        raise FileNotFoundError(
            image_path
        )

    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )


def run_final_demo_pipeline(
    nusc,
    scene_index=0,
    max_frames=3,
    tracking_threshold=8.0,
    prediction_horizon=5,
    prediction_dt=0.5
):
    """
    Run camera perception, LiDAR fusion, tracking, BEV mapping,
    occupancy mapping, and trajectory prediction across a scene.
    """

    perception = PerceptionPipeline()

    tracker = ObjectTracker(
        threshold=tracking_threshold
    )

    frames = []

    for frame_index, sample in iter_scene_samples(
        nusc,
        scene_index,
        max_frames
    ):

        cam_data = nusc.get(
            "sample_data",
            sample["data"]["CAM_FRONT"]
        )

        lidar_data = nusc.get(
            "sample_data",
            sample["data"]["LIDAR_TOP"]
        )

        image = load_camera_image(
            nusc,
            cam_data
        )

        detections = perception.run(
            image
        )

        fusion_results = run_fusion_from_detections(
            nusc,
            image,
            cam_data,
            lidar_data,
            detections
        )

        objects = fusion_results[
            "objects"
        ]

        valid_objects = filter_valid_objects(
            objects
        )

        suspicious_objects = find_suspicious_objects(
            objects
        )

        timestamp = (
            sample["timestamp"]
            / 1_000_000.0
        )

        tracked_objects = tracker.update(
            valid_objects,
            frame_index=frame_index,
            timestamp=timestamp
        )

        tracks = tracker.get_tracks()

        predictions = predict_all_tracks(
            tracks,
            prediction_horizon,
            prediction_dt
        )

        bev_objects = build_bev_scene(
            tracked_objects
        )

        occupancy_grid = populate_grid(
            create_grid(),
            bev_objects
        )

        frames.append(
            {
                "frame_index":
                frame_index,

                "timestamp":
                timestamp,

                "sample_token":
                sample["token"],

                "image":
                image,

                "detections":
                detections,

                "fusion_results":
                fusion_results,

                "objects":
                objects,

                "valid_objects":
                valid_objects,

                "suspicious_objects":
                suspicious_objects,

                "tracked_objects":
                tracked_objects,

                "tracks":
                [
                    dict(track)
                    for track in tracks
                ],

                "predictions":
                predictions,

                "bev_objects":
                bev_objects,

                "occupancy_grid":
                occupancy_grid
            }
        )

    return {
        "frames":
        frames,

        "tracks":
        tracker.get_tracks()
    }
