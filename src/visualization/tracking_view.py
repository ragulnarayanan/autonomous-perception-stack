import matplotlib.pyplot as plt

from bev.coordinate_conversion import (
    lidar_to_bev_plot
)


def visualize_tracks(
    tracked_objects
):

    plt.figure(
        figsize=(10, 10)
    )

    plt.scatter(
        0,
        0,
        marker="^",
        s=250,
        label="Ego Vehicle"
    )

    for obj in tracked_objects:

        x, y = lidar_to_bev_plot(
            obj["centroid"]
        )

        plt.scatter(
            x,
            y,
            s=100
        )

        plt.text(
            x,
            y,
            (
                f"ID {obj['track_id']}\n"
                f"{obj['class']}"
            )
        )

    plt.xlabel(
        "Lateral"
    )

    plt.ylabel(
        "Forward"
    )

    plt.title(
        "Tracked Objects"
    )

    plt.grid(True)

    plt.axis("equal")

    plt.show()
