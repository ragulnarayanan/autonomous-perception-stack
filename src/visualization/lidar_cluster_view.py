import matplotlib.pyplot as plt


def visualize_lidar_cluster(obj):

    points = obj["points_lidar"]

    x = points[0]
    y = points[1]

    plt.figure(figsize=(8,8))

    plt.scatter(
        x,
        y,
        s=3
    )

    plt.xlabel("Forward")
    plt.ylabel("Lateral")

    plt.title(
        f"{obj['class']} | "
        f"{obj['num_points']} pts"
    )

    plt.axis("equal")
    plt.grid(True)

    plt.show()