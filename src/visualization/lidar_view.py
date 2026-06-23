import matplotlib.pyplot as plt


def plot_lidar_top_view(
    point_cloud,
    save_path=None
):
    plt.figure(figsize=(10, 10))

    plt.scatter(
        point_cloud[0, :],
        point_cloud[1, :],
        s=0.2
    )

    plt.xlabel("X (Forward)")
    plt.ylabel("Y (Left)")
    plt.title("LiDAR Top View")

    plt.axis("equal")

    if save_path:
        plt.savefig(
            save_path,
            bbox_inches="tight"
        )

    plt.show()