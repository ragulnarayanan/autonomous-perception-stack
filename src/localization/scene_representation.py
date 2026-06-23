# src/localization/scene_representation.py

from localization.localizer import (
    localize_object
)

from localization.ego_coordinates import (
    get_ego_position
)


def build_scene(
    fused_objects
):

    scene = []

    for obj in fused_objects:

        localized = (
            localize_object(
                obj
            )
        )

        position = (
            get_ego_position(
                localized["centroid"]
            )
        )

        scene.append(
            {
                "class":
                localized["class"],

                "distance":
                localized["distance"],

                "position":
                position,

                "num_points":
                localized["num_points"]
            }
        )

    return scene