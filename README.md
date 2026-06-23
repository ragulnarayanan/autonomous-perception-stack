# 🚗 Autonomous Perception Stack

An end-to-end autonomous vehicle perception system built on the nuScenes dataset that combines camera and LiDAR sensors for object detection, sensor fusion, localization, tracking, trajectory prediction, and Bird's-Eye-View scene understanding.

The project recreates the core perception pipeline used in modern autonomous driving systems by transforming raw multi-sensor data into a structured understanding of the surrounding environment.

---

## Overview

Autonomous vehicles must continuously answer three questions:

1. What objects exist around the vehicle?
2. Where are those objects located in 3D space?
3. Where are those objects likely to move next?

This project implements a complete perception stack that addresses all three problems using camera imagery and LiDAR point clouds from the nuScenes autonomous driving dataset.

The system performs:

* Camera-based object detection and segmentation
* LiDAR point cloud processing
* Camera-LiDAR sensor fusion
* Object localization and distance estimation
* Bird's-Eye-View scene generation
* Multi-object tracking

---

# Project Architecture

```text
                    nuScenes Dataset
                            │
            ┌───────────────┴───────────────┐
            │                               │
            ▼                               ▼

      Camera Images                 LiDAR Point Clouds
            │                               │
            ▼                               ▼

    YOLOv8 Segmentation          Coordinate Transformations
            │                               │
            └───────────────┬───────────────┘
                            ▼

                 Camera-LiDAR Fusion
                            │
                            ▼

                 Object Localization
                            │
                            ▼

                 Bird's-Eye-View (BEV)
                            │
                            ▼

                 Multi-Object Tracking
                            │
                            ▼

                 Trajectory Prediction
                            │
                            ▼

                Scene Understanding
```

---

# Key Features

## Camera Perception

The perception module performs object detection and segmentation using YOLOv8.

Capabilities:

* Vehicle detection
* Pedestrian detection
* Traffic object segmentation
* Confidence estimation
* Instance-level masks

Outputs:

```python
{
    "class": "truck",
    "confidence": 0.91,
    "mask": ...
}
```

---

## LiDAR Processing

The LiDAR pipeline loads raw nuScenes point clouds and projects them into the camera image plane.

Implemented:

* LiDAR loading
* Homogeneous coordinates
* Sensor calibration
* Coordinate transformations
* Camera projection

Pipeline:

```text
LiDAR Frame
      ↓
Camera Frame
      ↓
Image Plane
```

---

## Camera-LiDAR Sensor Fusion

Camera detections are fused with projected LiDAR points to associate semantic information with geometric measurements.

Fusion workflow:

```text
Segmentation Mask
        ↓
Projected LiDAR Points
        ↓
Point Association
        ↓
3D Object Representation
```

Features:

* Instance-level fusion
* Confidence-based point ownership
* Duplicate point removal
* Sparse cluster filtering

---

## Object Localization

Each fused object is localized in 3D space.

Computed attributes:

* Object centroid
* Distance from ego vehicle
* 3D position
* Object dimensions

Example:

```python
{
    "position": {
        "x": 12.4,
        "y": -3.1,
        "z": 0.5
    },
    "distance": 12.8
}
```

---

## Bird's-Eye-View Mapping

The system generates a top-down representation of the environment.

Benefits:

* Spatial scene understanding
* Planning-friendly representation
* Object position visualization
* Ego-centric coordinate system

Generated outputs:

* Occupancy maps
* Object locations
* Ego vehicle reference frame

---

## Geometry Validation

Sensor fusion often produces noisy object geometry.

Validation tools were developed to:

* Inspect object dimensions
* Analyze LiDAR clusters
* Identify unrealistic geometry
* Validate object measurements

Example diagnostics:

```text
Truck
Length: 5.8m
Width : 2.6m
Height: 3.2m
```

---

## LiDAR Cluster Refinement

To improve object geometry quality, the project incorporates clustering-based refinement.

Methods:

* DBSCAN clustering
* Largest-cluster selection
* Outlier removal
* Sparse-point filtering

Pipeline:

```text
Fusion
   ↓
DBSCAN
   ↓
Largest Cluster
   ↓
Dimension Estimation
```

This significantly improves object dimension estimation by removing background structures and road points that may be included in segmentation masks.

---

## Multi-Object Tracking

Objects are tracked across consecutive frames.

Tracking features:

* Object association
* Track management
* Track IDs
* Track life-cycle handling

Example:

```text
Track 12 → Truck
Track 25 → Car
Track 31 → Pedestrian
```

Tracking provides temporal consistency beyond single-frame detections.

---

## Trajectory Prediction

Future object motion is estimated using historical track information.

Predictions include:

* Future position estimates
* Motion vectors
* Vehicle trajectory visualization

Applications:

* Path planning
* Collision avoidance
* Risk assessment

---

# Validation & Failure Analysis

A dedicated validation framework was developed to inspect perception quality.

Capabilities:

* Geometry inspection
* Cluster visualization
* Height analysis
* Distance verification
* False-positive investigation

Example findings:

* Segmentation masks occasionally absorb background geometry
* Sparse LiDAR regions increase localization uncertainty
* Cluster refinement significantly improves dimension estimation

---

# Visualizations

The project includes multiple visualization modules:

### Camera Detection

```text
Bounding Boxes
Segmentation Masks
Confidence Scores
```

### LiDAR Projection

```text
Projected LiDAR points
over camera imagery
```

### Fusion Visualization

```text
Segmentation Masks
+
LiDAR Points
```

### Localization View

```text
Object Positions
Distance Labels
```

### Bird's-Eye-View

```text
Top-down scene map
```

### Tracking View

```text
Track IDs
Motion History
```

---

# Dataset

Dataset:

nuScenes

Used Sensors:

* Front Camera
* Top LiDAR

nuScenes provides:

* Camera imagery
* LiDAR point clouds
* Calibration data
* Vehicle pose information
* Object annotations

---

# Technology Stack

### Computer Vision

* YOLOv8
* OpenCV

### Machine Learning

* PyTorch
* Scikit-learn

### Data Processing

* NumPy
* Pandas

### Autonomous Driving

* nuScenes SDK

### Visualization

* Matplotlib

### Geometry Processing

* DBSCAN
* Coordinate Transformations

---

# Repository Structure

```text
autonomous-perception-stack/

├── notebooks/
│   ├── 01_dataset_exploration.ipynb
│   ├── 02_lidar_projection.ipynb
│   ├── 03_camera_perception.ipynb
│   ├── 04_sensor_fusion.ipynb
│   ├── 05_localization.ipynb
│   ├── 06_bev_mapping.ipynb
│   ├── 07_tracking.ipynb
│   ├── 08_trajectory_prediction.ipynb
│   └── 09_validation.ipynb
│
├── src/
│   ├── perception/
│   ├── geometry/
│   ├── fusion/
│   ├── localization/
│   ├── tracking/
│   ├── prediction/
│   └── visualization/
│
├── outputs/
│   ├── images/
│   └── videos/
│
└── README.md
```

---

# Results

The completed perception stack successfully:

* Detects and segments road participants
* Projects LiDAR into image space
* Fuses camera and LiDAR information
* Localizes objects in 3D
* Generates Bird's-Eye-View scene representations
* Tracks objects across frames
* Predicts future object trajectories
* Validates perception quality using geometry diagnostics

The project demonstrates the complete perception workflow used in modern autonomous vehicle systems and serves as a foundation for future planning and decision-making modules.

---

# Author

Ragul Narayanan Magesh

MS Data Analytics Engineering
Northeastern University

GitHub:
https://github.com/ragulnarayanan
