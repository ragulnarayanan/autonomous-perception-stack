# src/bev/bev_mapper.py

import matplotlib.pyplot as plt


def create_bev_map(
    bev_objects,
    save_path=None
):

    plt.figure(
        figsize=(10, 10)
    )

    # Ego Vehicle

    plt.scatter(
        0,
        0,
        marker="^",
        s=250,
        label="Ego Vehicle"
    )

    for obj in bev_objects:

        x = obj["bev_x"]
        y = obj["bev_y"]

        plt.scatter(
            x,
            y,
            s=100
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
        "Forward Distance (m)"
    )

    plt.ylabel(
        "Lateral Position (m)"
    )

    plt.title(
        "Bird's Eye View Map"
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