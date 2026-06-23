# src/visualization/occupancy_view.py

import matplotlib.pyplot as plt


def visualize_occupancy_grid(
    grid,
    save_path=None
):

    plt.figure(
        figsize=(10, 10)
    )

    plt.imshow(
        grid,
        origin="lower"
    )

    plt.title(
        "Occupancy Grid Map"
    )

    plt.xlabel(
        "Forward"
    )

    plt.ylabel(
        "Lateral"
    )

    if save_path:

        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()