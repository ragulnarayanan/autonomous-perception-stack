# src/bev/scene_builder.py

from bev.coordinate_conversion import (
    lidar_to_bev
)


def build_bev_scene(
    objects
):

    bev_objects = []

    for obj in objects:

        centroid = obj["centroid"]

        bev_x, bev_y = (
            lidar_to_bev(
                centroid
            )
        )

        bev_objects.append(
            {
                **obj,

                "bev_x": bev_x,
                "bev_y": bev_y
            }
        )

    return bev_objects
