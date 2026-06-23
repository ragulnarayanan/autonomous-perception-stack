# src/bev/occupancy_mapper.py

import numpy as np


def world_to_grid(
    x,
    y,
    width,
    height,
    resolution
):

    gx = int(
        x / resolution
    )

    gy = int(
        (height // 2)
        - y / resolution
    )

    return gx, gy


def populate_grid(
    grid,
    bev_objects,
    resolution=1.0
):

    h, w = grid.shape

    for obj in bev_objects:

        x = obj["bev_x"]
        y = obj["bev_y"]

        gx, gy = (
            world_to_grid(
                x,
                y,
                w,
                h,
                resolution
            )
        )

        if (
            0 <= gx < w
            and
            0 <= gy < h
        ):
            grid[
                gy,
                gx
            ] = 1

    return grid