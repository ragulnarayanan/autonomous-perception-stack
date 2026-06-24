# src/visualization/occupancy_view.py

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def visualize_occupancy_grid(
    grid,
    save_path=None
):

    fig, ax = plt.subplots(
        figsize=(10, 10)
    )

    cmap = ListedColormap(
        [
            "white",
            "black"
        ]
    )

    ax.imshow(
        grid,
        origin="lower",
        cmap=cmap,
        vmin=0,
        vmax=1
    )

    ax.set_title(
        "Occupancy Grid Map"
    )

    ax.set_xlabel(
        "Forward"
    )

    ax.set_ylabel(
        "Lateral"
    )

    ax.set_xticks(
        range(
            0,
            grid.shape[1],
            5
        )
    )

    ax.set_yticks(
        range(
            0,
            grid.shape[0],
            5
        )
    )

    ax.grid(
        color="lightgray",
        linewidth=0.5
    )

    if save_path:

        fig.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
