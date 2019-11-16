import numpy as np


def orient(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    return a[0]*b[1] + b[0]*c[1] + c[0]*a[1] - a[0]*c[1] - b[0]*a[1] - c[0]*b[1]


def dist2(a: np.ndarray, b: np.ndarray) -> float:
    return sum(np.square(b - a))
