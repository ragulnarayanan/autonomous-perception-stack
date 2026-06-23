# src/visualization/bev_view.py

from bev.bev_mapper import (
    create_bev_map
)


def visualize_bev(
    bev_objects,
    save_path=None
):

    create_bev_map(
        bev_objects,
        save_path
    )