import matplotlib.pyplot as plt
import matplotlib.patches as patches


def visualize_fusion(
    image,
    objects,
    save_path=None
):
    """
    Visualize Camera-LiDAR Fusion.

    Parameters
    ----------
    image : np.ndarray

    objects : list
        Output from extract_object_properties()

    save_path : str
    """

    fig, ax = plt.subplots(
        figsize=(16, 9)
    )

    ax.imshow(image)

    for obj in objects:

        # -----------------------
        # Draw LiDAR Points
        # -----------------------

        if "u" in obj and "v" in obj:
            ax.scatter(
                obj["u"],
                obj["v"],
                s=5,
                alpha=0.8
            )

        # -----------------------
        # Draw Bounding Box
        # -----------------------

        if "bbox" in obj:

            x1, y1, x2, y2 = obj["bbox"]

            rect = patches.Rectangle(
                (x1, y1),
                x2 - x1,
                y2 - y1,
                linewidth=2,
                fill=False
            )

            ax.add_patch(rect)

        # -----------------------
        # Label
        # -----------------------

        if "bbox" in obj:

            label = (
                f"{obj['class']} | "
                f"{obj['distance']:.1f}m | "
                f"{obj['num_points']} pts"
            )

            ax.text(
                max(
                    obj["bbox"][0],
                    0
                ),
                max(
                    obj["bbox"][1],
                    12
                ),
                label,
                fontsize=8,
                bbox=dict(
                    facecolor="white",
                    alpha=0.8
                )
            )

    ax.set_title(
        "Camera-LiDAR Fusion"
    )

    ax.axis("off")

    plt.tight_layout()

    if save_path:

        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
