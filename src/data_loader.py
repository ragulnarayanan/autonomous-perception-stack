from nuscenes.nuscenes import NuScenes
from pathlib import Path


def load_nuscenes(version="v1.0-mini"):
    project_root = Path(__file__).resolve().parent.parent

    dataroot = project_root / "data" / "nuscenes"

    print(f"Loading nuScenes from: {dataroot}")

    nusc = NuScenes(
        version=version,
        dataroot=str(dataroot),
        verbose=True
    )

    return nusc