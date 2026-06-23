# src/tracking/track_utils.py


def summarize_tracks(
    tracked_objects
):

    summary = {}

    for obj in tracked_objects:

        tid = (
            obj["track_id"]
        )

        summary[tid] = (
            obj["class"]
        )

    return summary