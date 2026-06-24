# src/prediction/trajectory.py

import numpy as np


def predict_track_trajectory(
    track,
    horizon_steps=5,
    dt=0.5
):
    """
    Predict future track centroids with a constant-velocity model.
    """

    centroid = np.asarray(
        track["centroid"],
        dtype=float
    )

    velocity = np.asarray(
        track.get(
            "velocity",
            np.zeros(3)
        ),
        dtype=float
    )

    trajectory = []

    for step in range(1, horizon_steps + 1):

        future = (
            centroid
            +
            velocity
            *
            dt
            *
            step
        )

        trajectory.append(
            future
        )

    return trajectory


def predict_all_tracks(
    tracks,
    horizon_steps=5,
    dt=0.5
):
    """
    Attach predicted trajectories to tracker state dictionaries.
    """

    predictions = []

    for track in tracks:

        predictions.append(
            {
                "track_id":
                track["track_id"],

                "class":
                track["class"],

                "centroid":
                track["centroid"],

                "velocity":
                track.get(
                    "velocity",
                    np.zeros(3)
                ),

                "trajectory":
                predict_track_trajectory(
                    track,
                    horizon_steps,
                    dt
                )
            }
        )

    return predictions
