from pathlib import Path

from ultralytics import YOLO


def resolve_model_path(
    model_path
):
    path = Path(model_path)

    if path.exists():
        return str(path)

    project_root = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    candidates = [
        project_root / model_path,
        project_root / "notebooks" / model_path
    ]

    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    return model_path


class SegmentationModel:
    """
    YOLO Segmentation Wrapper
    """

    def __init__(
        self,
        model_path="yolo11n-seg.pt"
    ):
        self.model = YOLO(
            resolve_model_path(
                model_path
            )
        )

    def predict(
        self,
        image,
        conf=0.25,
        iou=0.45
    ):
        """
        Run segmentation inference.

        Parameters
        ----------
        image : np.ndarray

        conf : float

        iou : float

        Returns
        -------
        ultralytics results
        """

        results = self.model.predict(
            source=image,
            conf=conf,
            iou=iou,
            verbose=False
        )

        return results
