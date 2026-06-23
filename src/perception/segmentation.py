from ultralytics import YOLO


class SegmentationModel:
    """
    YOLO Segmentation Wrapper
    """

    def __init__(
        self,
        model_path="yolo11n-seg.pt"
    ):
        self.model = YOLO(model_path)

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