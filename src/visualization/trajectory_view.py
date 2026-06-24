# src/visualization/trajectory_view.py

import matplotlib.pyplot as plt

from bev.coordinate_conversion import (
    lidar_to_bev_plot
)


def visualize_trajectories(
    tracked_objects,
    predictions,
    save_path=None
):
    """
    Plot current tracked objects and predicted paths in BEV.
    """

    fig, ax = plt.subplots(
        figsize=(10, 10)
    )

    ax.scatter(
        0,
        0,
        marker="^",
        s=250,
        label="Ego Vehicle"
    )

    prediction_by_id = {
        pred["track_id"]: pred
        for pred in predictions
    }

    for obj in tracked_objects:

        x, y = lidar_to_bev_plot(
            obj["centroid"]
        )

        ax.scatter(
            x,
            y,
            s=100
        )

        ax.text(
            x,
            y,
            (
                f"ID {obj['track_id']}\n"
                f"{obj['class']}"
            )
        )

        pred = prediction_by_id.get(
            obj["track_id"]
        )

        if pred is None:
            continue

        future_points = [
            lidar_to_bev_plot(
                point
            )
            for point in pred["trajectory"]
        ]

        if not future_points:
            continue

        future_x = [
            point[0]
            for point in future_points
        ]

        future_y = [
            point[1]
            for point in future_points
        ]

        ax.plot(
            future_x,
            future_y,
            linestyle="--",
            marker="o",
            linewidth=1.5
        )

    ax.set_xlabel(
        "Lateral Position (m)"
    )

    ax.set_ylabel(
        "Forward Distance (m)"
    )

    ax.set_title(
        "Tracked Objects and Predicted Trajectories"
    )

    ax.grid(True)
    ax.axis("equal")

    if save_path:

        fig.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
