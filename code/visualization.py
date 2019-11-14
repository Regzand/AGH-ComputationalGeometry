from typing import List, Any, Tuple

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import to_rgba


mpl.rcParams['animation.html'] = 'jshtml'


def plot_points(points: np.ndarray, annotations: List[str] = [], keep_aspect: bool = True, **kwargs):

    # points
    if len(points):
        plt.scatter(*zip(*points), **kwargs)

    # aspect ratio
    if keep_aspect:
        plt.axis('equal')

    # annotations
    for p, text in zip(points, annotations):
        plt.annotate(text, p, (5, 5), textcoords='offset pixels')


def plot_segments(segments: np.ndarray, colors: Any = None, zorder: int = 1, **kwargs):

    # handle colors conversion
    if isinstance(colors, list):
        colors = [to_rgba(c) for c in colors]
    elif colors is not None:
        colors = [to_rgba(colors)] * len(segments)
    
    # plot segments using collection for better performance
    plt.gca().add_collection(LineCollection(segments, colors=colors, zorder=zorder, **kwargs))
    plt.gca().autoscale(True)


def plot_chain(points: np.ndarray, closed: bool = False, **kwargs):

    # create segments
    segments = [(points[i - 1], points[i]) for i in range(1, len(points))]

    # close loop if requested
    if closed:
        segments.append((points[-1], points[0]))

    plot_segments(segments, **kwargs)
