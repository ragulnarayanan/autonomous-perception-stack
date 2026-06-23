# src/fusion/cluster_filter.py

import numpy as np
from sklearn.cluster import DBSCAN


def largest_cluster(
    points,
    eps=1.0,
    min_samples=10,
    return_mask=False
):
    """
    Keep largest LiDAR cluster.

    points:
        (3, N)
    """

    if points.shape[1] < min_samples:
        if return_mask:
            return points, np.ones(points.shape[1], dtype=bool)
        return points

    xyz = points.T

    clustering = DBSCAN(
        eps=eps,
        min_samples=min_samples
    )

    labels = clustering.fit_predict(xyz)

    valid_labels = [
        label
        for label in np.unique(labels)
        if label != -1
    ]

    if len(valid_labels) == 0:
        if return_mask:
            return points, np.ones(points.shape[1], dtype=bool)
        return points

    largest_label = max(
        valid_labels,
        key=lambda l: np.sum(labels == l)
    )

    cluster_mask = (
        labels == largest_label
    )

    if return_mask:
        return points[:, cluster_mask], cluster_mask

    return points[:, cluster_mask]
