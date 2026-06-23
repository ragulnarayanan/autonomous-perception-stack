# src/tracking/tracker.py

from tracking.association import (
    associate_tracks
)

from tracking.track_manager import (
    TrackManager
)


class ObjectTracker:

    def __init__(
        self,
        threshold=3.0
    ):

        self.threshold = (
            threshold
        )

        self.manager = (
            TrackManager()
        )

    def update(
        self,
        objects
    ):

        tracks = (
            self.manager.get_tracks()
        )

        if len(tracks) == 0:

            tracked_objects = []

            for obj in objects:

                track = (
                    self.manager
                    .create_track(
                        obj
                    )
                )

                tracked_objects.append(
                    {
                        **obj,

                        "track_id":
                        track[
                            "track_id"
                        ]
                    }
                )

            return tracked_objects

        matches = (
            associate_tracks(
                objects,
                tracks,
                self.threshold
            )
        )

        tracked_objects = []

        matched_objects = set()

        for (
            obj_idx,
            track_idx
        ) in matches:

            obj = objects[
                obj_idx
            ]

            self.manager.update_track(
                track_idx,
                obj
            )

            tracked_objects.append(
                {
                    **obj,

                    "track_id":
                    tracks[
                        track_idx
                    ]["track_id"]
                }
            )

            matched_objects.add(
                obj_idx
            )

        for idx, obj in enumerate(
            objects
        ):

            if idx in matched_objects:
                continue

            track = (
                self.manager
                .create_track(
                    obj
                )
            )

            tracked_objects.append(
                {
                    **obj,

                    "track_id":
                    track[
                        "track_id"
                    ]
                }
            )

        return tracked_objects