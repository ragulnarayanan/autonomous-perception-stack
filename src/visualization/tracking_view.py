import matplotlib.pyplot as plt


def visualize_tracks(
    tracked_objects
):

    plt.figure(
        figsize=(10, 10)
    )

    plt.scatter(
        0,
        0,
        marker="^",
        s=250,
        label="Ego Vehicle"
    )

    for obj in tracked_objects:

        x = obj["centroid"][2]
        y = obj["centroid"][0]

        plt.scatter(
            x,
            y,
            s=100
        )

        plt.text(
            x,
            y,
            (
                f"ID {obj['track_id']}\n"
                f"{obj['class']}"
            )
        )

    plt.xlabel(
        "Forward"
    )

    plt.ylabel(
        "Lateral"
    )

    plt.title(
        "Tracked Objects"
    )

    plt.grid(True)

    plt.axis("equal")

    plt.show()