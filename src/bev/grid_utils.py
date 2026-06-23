# src/bev/grid_utils.py

import numpy as np


def occupancy_statistics(
    grid
):

    occupied = np.sum(
        grid == 1
    )

    total = grid.size

    return {
        "occupied":
        int(occupied),

        "free":
        int(total - occupied),

        "occupancy_ratio":
        float(occupied / total)
    }