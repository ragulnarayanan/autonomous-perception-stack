import json
import sys
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.append(
        str(SRC_ROOT)
    )

from data_loader import load_nuscenes
from fusion.validation import create_fusion_summary
from pipeline.final_demo_pipeline import run_final_demo_pipeline
from visualization.fusion_view import visualize_fusion
from visualization.occupancy_view import visualize_occupancy_grid
from visualization.trajectory_view import visualize_trajectories


def to_list(
    value
):
    if isinstance(
        value,
        np.ndarray
    ):
        return value.tolist()

    if isinstance(
        value,
        list
    ):
        return [
            to_list(item)
            for item in value
        ]

    if isinstance(
        value,
        dict
    ):
        return {
            key: to_list(item)
            for key, item in value.items()
        }

    return value


def summarize_frame(
    frame
):
    return {
        "frame_index":
        frame["frame_index"],

        "timestamp":
        frame["timestamp"],

        "sample_token":
        frame["sample_token"],

        "detections":
        len(frame["detections"]),

        "raw_fused_objects":
        len(frame["objects"]),

        "valid_tracked_objects":
        len(frame["tracked_objects"]),

        "suspicious_objects":
        [
            {
                "class":
                obj["class"],

                "distance":
                obj["distance"],

                "num_points":
                obj["num_points"],

                "dimensions":
                obj["dimensions"]
            }
            for obj in frame["suspicious_objects"]
        ],

        "objects":
        [
            {
                "class":
                obj["class"],

                "confidence":
                obj["confidence"],

                "track_id":
                obj.get(
                    "track_id"
                ),

                "distance":
                obj["distance"],

                "num_points":
                obj["num_points"],

                "position":
                obj["position"],

                "dimensions":
                obj["dimensions"]
            }
            for obj in frame["tracked_objects"]
        ],

        "predictions":
        [
            {
                "track_id":
                pred["track_id"],

                "class":
                pred["class"],

                "velocity":
                to_list(
                    pred["velocity"]
                ),

                "trajectory":
                to_list(
                    pred["trajectory"]
                )
            }
            for pred in frame["predictions"]
        ]
    }


def main():
    output_images = PROJECT_ROOT / "outputs" / "images"
    output_json = PROJECT_ROOT / "outputs" / "json"

    output_images.mkdir(
        parents=True,
        exist_ok=True
    )

    output_json.mkdir(
        parents=True,
        exist_ok=True
    )

    nusc = load_nuscenes()

    results = run_final_demo_pipeline(
        nusc,
        scene_index=0,
        max_frames=3
    )

    frames = results[
        "frames"
    ]

    if not frames:
        raise RuntimeError(
            "No frames were processed."
        )

    final_frame = frames[
        -1
    ]

    visualize_fusion(
        final_frame["image"],
        final_frame["tracked_objects"],
        save_path=str(
            output_images / "final_demo_fusion.png"
        )
    )

    visualize_trajectories(
        final_frame["tracked_objects"],
        final_frame["predictions"],
        save_path=str(
            output_images / "final_demo_trajectories.png"
        )
    )

    visualize_occupancy_grid(
        final_frame["occupancy_grid"],
        save_path=str(
            output_images / "final_demo_occupancy.png"
        )
    )

    summary = {
        "frames_processed":
        len(frames),

        "final_frame_summary":
        create_fusion_summary(
            final_frame["tracked_objects"]
        ).to_dict(
            orient="records"
        ),

        "frames":
        [
            summarize_frame(
                frame
            )
            for frame in frames
        ]
    }

    summary_path = (
        output_json
        /
        "final_demo_summary.json"
    )

    summary_path.write_text(
        json.dumps(
            to_list(
                summary
            ),
            indent=2
        )
    )

    print(
        f"Processed {len(frames)} frames"
    )

    print(
        f"Saved {summary_path}"
    )

    print(
        create_fusion_summary(
            final_frame["tracked_objects"]
        ).to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()
