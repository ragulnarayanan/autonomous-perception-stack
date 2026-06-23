# src/tracking/track_manager.py


class TrackManager:

    def __init__(self):

        self.next_track_id = 0

        self.tracks = []

    def create_track(
        self,
        obj
    ):

        track = {
            "track_id":
            self.next_track_id,

            "centroid":
            obj["centroid"],

            "class":
            obj["class"],

            "age": 1
        }

        self.tracks.append(
            track
        )

        self.next_track_id += 1

        return track

    def update_track(
        self,
        track_idx,
        obj
    ):

        self.tracks[
            track_idx
        ]["centroid"] = (
            obj["centroid"]
        )

        self.tracks[
            track_idx
        ]["class"] = (
            obj["class"]
        )

        self.tracks[
            track_idx
        ]["age"] += 1

    def get_tracks(
        self
    ):

        return self.tracks