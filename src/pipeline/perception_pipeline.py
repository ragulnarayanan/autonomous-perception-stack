from perception.inference import (
    PerceptionPipeline
)


def run_perception_pipeline(
    image
):
    """
    Run camera perception pipeline.

    Returns
    -------
    detections
    """

    pipeline = (
        PerceptionPipeline()
    )

    detections = (
        pipeline.run(
            image
        )
    )

    return detections