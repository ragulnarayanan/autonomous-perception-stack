# src/visualization/localization_view.py

def visualize_localization(
    objects,
    max_objects=20
):
    """
    Print localized object states.
    """

    print("\nOBJECT LOCALIZATION RESULTS")
    print("=" * 80)

    for idx, obj in enumerate(
        objects[:max_objects]
    ):

        print(
            f"\nObject {idx+1}"
        )

        print(
            f"Class: {obj['class']}"
        )

        print(
            f"Distance: "
            f"{obj['distance']:.2f} m"
        )

        print(
            f"Position:"
        )

        print(
            f"  X: {obj['position']['x']:.2f} m"
        )

        print(
            f"  Y: {obj['position']['y']:.2f} m"
        )

        print(
            f"  Z: {obj['position']['z']:.2f} m"
        )

        print(
            f"Dimensions:"
        )

        print(
            f"  Length: "
            f"{obj['dimensions']['length']:.2f} m"
        )

        print(
            f"  Width: "
            f"{obj['dimensions']['width']:.2f} m"
        )

        print(
            f"  Height: "
            f"{obj['dimensions']['height']:.2f} m"
        )

        print(
            f"LiDAR Points: "
            f"{obj['num_points']}"
        )

        print("-" * 80)

import matplotlib.pyplot as plt

from bev.coordinate_conversion import (
    lidar_to_bev_plot
)


def plot_localized_objects(
    objects,
    save_path=None
):

    plt.figure(
        figsize=(10, 10)
    )

    plt.scatter(
        0,
        0,
        marker="^",
        s=200,
        label="Ego Vehicle"
    )

    for obj in objects:

        x, y = lidar_to_bev_plot(
            obj["centroid"]
        )

        plt.scatter(
            x,
            y,
            s=60
        )

        plt.text(
            x,
            y,
            (
                f"{obj['class']}\n"
                f"{obj['distance']:.1f}m"
            )
        )

    plt.xlabel(
        "Lateral Distance (m)"
    )

    plt.ylabel(
        "Forward Distance (m)"
    )

    plt.title(
        "Localized Objects"
    )

    plt.grid(True)

    plt.axis("equal")

    if save_path:

        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
