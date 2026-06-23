import numpy as np
from pyquaternion import Quaternion


def build_transform_matrix(translation, rotation):
    """
    Build 4x4 homogeneous transformation matrix.

    Parameters
    ----------
    translation : list
        [x, y, z]

    rotation : list
        Quaternion [w, x, y, z]

    Returns
    -------
    np.ndarray
        4x4 transformation matrix
    """

    T = np.eye(4)

    T[:3, :3] = Quaternion(rotation).rotation_matrix
    T[:3, 3] = np.array(translation)

    return T


def invert_transform(T):
    """
    Invert homogeneous transform.
    """

    return np.linalg.inv(T)


def apply_transform(points, T):
    """
    Apply transformation matrix.

    Parameters
    ----------
    points : np.ndarray
        shape (4, N)

    T : np.ndarray
        shape (4, 4)
    """

    return T @ points