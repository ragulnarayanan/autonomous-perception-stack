import matplotlib.pyplot as plt


def visualize_projection(
    image,
    u,
    v,
    save_path=None
):

    plt.figure(figsize=(14, 8))

    plt.imshow(image)

    plt.scatter(
        u,
        v,
        s=0.3,
        alpha=0.8
    )

    plt.xlim(0, image.shape[1])
    plt.ylim(image.shape[0], 0)

    plt.title(
        "LiDAR Projection on Camera Image"
    )

    if save_path:
        plt.savefig(
            save_path,
            bbox_inches="tight"
        )

    plt.show()