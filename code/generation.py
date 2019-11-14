from typing import List

import numpy as np


def random_points_plane(n: int, corner1: np.ndarray, corner2: np.ndarray) -> np.ndarray:
    x = np.random.uniform(size=(n, 1), low=min(corner1[0], corner2[0]), high=max(corner1[0], corner2[0]))
    y = np.random.uniform(size=(n, 1), low=min(corner1[1], corner2[1]), high=max(corner1[1], corner2[1]))
    return np.hstack((x, y))


def random_points_circle(n: int, radius: float, center: np.ndarray) -> np.ndarray:
    angles = np.random.uniform(low=0, high=2 * np.pi, size=n)
    points = np.full((n, 2), radius, dtype='d')
    points[:, 0] *= np.cos(angles)
    points[:, 1] *= np.sin(angles)
    points[:, 0] += center[0]
    points[:, 1] += center[1]
    return points


def random_points_segment(n: int, point1: np.ndarray, point2: np.ndarray) -> np.ndarray:
    t = np.random.uniform(size=(n, 1))
    return (1 - t) * point1 + t * point2


def random_points_polygon(n: int, points: List[np.ndarray]) -> np.ndarray:
    return np.vstack([
        random_points_segment(n // len(points), points[i-1], points[i])
        for i in range(len(points))
    ])


def random_points_weird(n_edge: int, n_diagonal: int,
                        p1: np.ndarray, p2: np.ndarray, p3: np.ndarray, p4: np.ndarray) -> np.ndarray:
    return np.vstack([
        [p1], [p2], [p3], [p4],
        random_points_segment(n_edge, p1, p2),
        random_points_segment(n_edge, p2, p3),
        random_points_segment(n_diagonal, p1, p3),
        random_points_segment(n_diagonal, p2, p4),
    ])

def random_segments_plane(n: int, corner1: np.ndarray, corner2: np.ndarray) -> np.ndarray:
    return np.resize(random_points_plane(2 * n, corner1, corner2), (n, 2, 2))
