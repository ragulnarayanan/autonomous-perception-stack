

from perception.segmentation import (
    SegmentationModel
)

from perception.detections import (
    extract_detections
)


class PerceptionPipeline:

    def __init__(self):

        self.segmenter = (
            SegmentationModel()
        )

    def run(
        self,
        image
    ):

        results = (
            self.segmenter.predict(
                image
            )
        )

        detections = (
            extract_detections(
                results
            )
        )

        return detections