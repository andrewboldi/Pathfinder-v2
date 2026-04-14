#!/usr/bin/env python3
"""Pathfinder: Scenic driving route finder using percolation theory.

Usage:
    python main.py START END ECCENTRICITY SCENICNESS_CUTOFF N_CLUSTERS

Example:
    python main.py 37.538288,-122.308576 37.561886,-122.3522 0.4 0.5 10
"""
import sys
from matplotlib import pyplot as plt

from core.percolation import run_percolation_pipeline


def main():
    try:
        start = sys.argv[1]
        end = sys.argv[2]
        eccentricity = float(sys.argv[3])
        p = float(sys.argv[4])
        n_clusters = int(sys.argv[5])
    except (IndexError, ValueError):
        print(
            "Usage: python main.py START END ECCENTRICITY SCENICNESS_CUTOFF N_CLUSTERS\n"
            "  START/END:      lat,lon (e.g. 37.538288,-122.308576)\n"
            "  ECCENTRICITY:   ellipse bound eccentricity (0-1)\n"
            "  SCENICNESS:     scenicness p-value cutoff (0-1)\n"
            "  N_CLUSTERS:     number of scenic clusters to visit"
        )
        sys.exit(1)

    run_percolation_pipeline(start, end, eccentricity, p, n_clusters)
    plt.show()


if __name__ == "__main__":
    main()
