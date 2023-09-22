import datetime

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import MinMaxScaler


def find_clusters_DBSCAN(
    timestamps: list[int], distances: list[int], eps=0.02, min_samples=6
) -> list[int]:
    """
    Uses DBSCAN to find clusters, assigning a cluster ID to each point.

    Args:
        timestamps (list[int]): Time-series data of each point represented in
                                integer format.
        distances (list[int]): Distance data of each point.
        eps (float, optional): Epsilon parameter of DBSCAN. Defaults to 0.02.
        min_samples (int, optional): min_samples parameter of DBSCAN. Defaults
                                     to 6.

    Returns:
        list[int]: THe cluster ID for each point.
    """
    X = np.column_stack((timestamps, distances))
    scaler = MinMaxScaler()
    X_normalized = scaler.fit_transform(X)
    model = DBSCAN(eps=eps, min_samples=min_samples, metric="precomputed")
    distance_matrix = euclidean_distances(X_normalized)
    clusters = model.fit_predict(distance_matrix)
    return clusters


def find_cluster_averages_DBSCAN(
    timings: list[datetime.datetime], distances: list[int], clusters: list[int]
) -> tuple[list]:
    """
    Returns the average timings and distances for each cluster.

    Args:
        timings (list[datetime.datetime]): The time that each point was recorded.
        distances (list[int]): The distances of each point.
        clusters (list[int]): The cluster ID for each point.

    Returns:
        tuple[list]: _description_
    """
    df = pd.DataFrame(
        {"timings": timings, "distances": distances, "clusters": clusters}
    )
    cluster_averages = (
        df.groupby("clusters")
        .agg({"timings": "mean", "distances": "mean"})
        .reset_index()
    )
    return cluster_averages["timings"], cluster_averages["distances"]
