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
        threshold=5.0,
        max_missed=2,
        class_aware=True
    ):

        self.threshold = (
            threshold
        )

        self.max_missed = (
            max_missed
        )

        self.class_aware = (
            class_aware
        )

        self.manager = (
            TrackManager()
        )

    def update(
        self,
        objects,
        frame_index=0,
        timestamp=None
    ):

        tracks = list(
            self.manager.get_tracks()
        )

        if len(tracks) == 0:

            tracked_objects = []

            for obj in objects:

                track = (
                    self.manager
                    .create_track(
                        obj,
                        frame_index,
                        timestamp
                    )
                )

                tracked_objects.append(
                    {
                        **obj,

                        "track_id":
                        track[
                            "track_id"
                        ],

                        "velocity":
                        track[
                            "velocity"
                        ],

                        "track_age":
                        track[
                            "age"
                        ]
                    }
                )

            return tracked_objects

        matches = (
            associate_tracks(
                objects,
                tracks,
                self.threshold,
                self.class_aware
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
                obj,
                frame_index,
                timestamp
            )

            tracked_objects.append(
                {
                    **obj,

                    "track_id":
                    tracks[
                        track_idx
                    ]["track_id"],

                    "velocity":
                    tracks[
                        track_idx
                    ]["velocity"],

                    "track_age":
                    tracks[
                        track_idx
                    ]["age"]
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
                    obj,
                    frame_index,
                    timestamp
                )
            )

            tracked_objects.append(
                {
                    **obj,

                    "track_id":
                    track[
                        "track_id"
                    ],

                    "velocity":
                    track[
                        "velocity"
                    ],

                    "track_age":
                    track[
                        "age"
                    ]
                }
            )

        matched_tracks = {
            track_idx
            for _, track_idx in matches
        }

        for track_idx, _ in enumerate(
            tracks
        ):
            if track_idx not in matched_tracks:
                self.manager.mark_missed(
                    track_idx
                )

        self.manager.prune_tracks(
            self.max_missed
        )

        return tracked_objects

    def get_tracks(
        self
    ):

        return self.manager.get_tracks()
