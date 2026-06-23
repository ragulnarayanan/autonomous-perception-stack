import matplotlib.pyplot as plt
import matplotlib.patches as patches


def visualize_object_fusion(
    image,
    obj
):

    fig, ax = plt.subplots(
        figsize=(16, 9)
    )

    ax.imshow(image)

    ax.scatter(
        obj["u"],
        obj["v"],
        s=5,
        c="red",
        alpha=0.7
    )

    if "bbox" in obj:

        xmin, ymin, xmax, ymax = (
            obj["bbox"]
        )

        rect = patches.Rectangle(
            (
                xmin,
                ymin
            ),
            xmax - xmin,
            ymax - ymin,
            fill=False,
            linewidth=2
        )

        ax.add_patch(rect)

    ax.set_title(
        f"{obj['class']} | "
        f"{obj['num_points']} points | "
        f"{obj['distance']:.2f}m"
    )

    ax.axis("off")

    plt.show()