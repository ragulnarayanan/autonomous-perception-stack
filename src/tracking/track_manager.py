# src/tracking/track_manager.py

import numpy as np


class TrackManager:

    def __init__(self):

        self.next_track_id = 0

        self.tracks = []

    def create_track(
        self,
        obj,
        frame_index=0,
        timestamp=None
    ):

        centroid = np.asarray(
            obj["centroid"],
            dtype=float
        )

        track = {
            "track_id":
            self.next_track_id,

            "centroid":
            centroid,

            "class":
            obj["class"],

            "age": 1,

            "hits": 1,

            "missed": 0,

            "first_frame":
            frame_index,

            "last_frame":
            frame_index,

            "last_timestamp":
            timestamp,

            "velocity":
            np.zeros(3),

            "history":
            [
                {
                    "frame_index":
                    frame_index,

                    "timestamp":
                    timestamp,

                    "centroid":
                    centroid.copy()
                }
            ]
        }

        self.tracks.append(
            track
        )

        self.next_track_id += 1

        return track

    def update_track(
        self,
        track_idx,
        obj,
        frame_index=0,
        timestamp=None
    ):

        track = self.tracks[
            track_idx
        ]

        previous_centroid = np.asarray(
            track["centroid"],
            dtype=float
        )

        centroid = np.asarray(
            obj["centroid"],
            dtype=float
        )

        previous_timestamp = track.get(
            "last_timestamp"
        )

        dt = 1.0

        if (
            timestamp is not None
            and previous_timestamp is not None
        ):
            dt = max(
                float(timestamp - previous_timestamp),
                1e-6
            )

        velocity = (
            centroid
            -
            previous_centroid
        ) / dt

        track["centroid"] = centroid

        track["class"] = (
            obj["class"]
        )

        track["age"] += 1
        track["hits"] += 1
        track["missed"] = 0
        track["last_frame"] = frame_index
        track["last_timestamp"] = timestamp
        track["velocity"] = velocity

        track["history"].append(
            {
                "frame_index":
                frame_index,

                "timestamp":
                timestamp,

                "centroid":
                centroid.copy()
            }
        )

    def mark_missed(
        self,
        track_idx
    ):

        self.tracks[
            track_idx
        ]["missed"] += 1

        self.tracks[
            track_idx
        ]["age"] += 1

    def prune_tracks(
        self,
        max_missed=2
    ):

        self.tracks = [
            track
            for track in self.tracks
            if track["missed"] <= max_missed
        ]

    def get_tracks(
        self
    ):

        return self.tracks
