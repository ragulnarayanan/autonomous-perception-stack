# src/perception/detections.py

import numpy as np


def extract_detections(results):

    result = results[0]

    detections = []

    if result.boxes is None:
        return detections

    masks = None

    if result.masks is not None:
        masks = result.masks.data.cpu().numpy()

    for idx, box in enumerate(result.boxes):

        class_id = int(
            box.cls.cpu().numpy()[0]
        )

        confidence = float(
            box.conf.cpu().numpy()[0]
        )

        bbox = (
            box.xyxy
            .cpu()
            .numpy()[0]
            .tolist()
        )

        class_name = (
            result.names[class_id]
        )

        mask = None

        if masks is not None:
            mask = masks[idx]

        detections.append(
            {
                "class": class_name,
                "confidence": confidence,
                "bbox": bbox,
                "mask": mask
            }
        )

    return detections