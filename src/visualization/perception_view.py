import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def visualize_detections(
    image,
    detections,
    show_masks=True,
    save_path=None
):
    """
    Visualize YOLO detections and segmentation masks.

    Parameters
    ----------
    image : np.ndarray
        Original RGB image

    detections : list
        Output from extract_detections()

    show_masks : bool

    save_path : str
    """

    fig, ax = plt.subplots(
        figsize=(16, 9)
    )

    ax.imshow(image)

    # Single overlay for all masks
    overlay = np.zeros(
        (
            image.shape[0],
            image.shape[1],
            4
        ),
        dtype=np.float32
    )

    for det in detections:

        # -------------------------
        # Bounding Box
        # -------------------------

        x1, y1, x2, y2 = det["bbox"]

        rect = patches.Rectangle(
            (x1, y1),
            x2 - x1,
            y2 - y1,
            linewidth=2,
            fill=False
        )

        ax.add_patch(rect)

        label = (
            f"{det['class']} "
            f"{det['confidence']:.2f}"
        )

        ax.text(
            x1,
            y1,
            label,
            fontsize=8,
            bbox=dict(
                facecolor="white",
                alpha=0.8
            )
        )

        # -------------------------
        # Segmentation Mask
        # -------------------------

        if (
            show_masks
            and det["mask"] is not None
        ):

            mask = det["mask"]

            # Resize mask to original image
            mask = cv2.resize(
                mask.astype(np.uint8),
                (
                    image.shape[1],
                    image.shape[0]
                ),
                interpolation=cv2.INTER_NEAREST
            )

            overlay[:, :, 0] += (
                mask * 1.0
            )

            overlay[:, :, 3] += (
                mask * 0.12
            )

    overlay[:, :, 0] = np.clip(
        overlay[:, :, 0],
        0,
        1
    )

    overlay[:, :, 3] = np.clip(
        overlay[:, :, 3],
        0,
        0.45
    )

    ax.imshow(overlay)

    ax.set_title(
        "YOLO Segmentation Results"
    )

    ax.axis("off")

    plt.tight_layout()

    if save_path:

        plt.savefig(
            save_path,
            bbox_inches="tight",
            dpi=300
        )

    plt.show()