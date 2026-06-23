# src/bev/occupancy_grid.py

import numpy as np


def create_grid(
    width=50,
    height=50,
    resolution=1.0
):

    return np.zeros(
        (height, width),
        dtype=np.uint8
    )