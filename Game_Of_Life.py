"""
Conway's game of life
"""

import sys
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class GameOfLife(object):
    def __init__(self, shape, initial):

        self.shape = shape
        self.initial = initial

        self.create_lattice()

    def create_lattice(self) -> None:
        """Create an NxN lattice with given starting conditions"""

        if self.initial == "random":
            self.lattice = np.random.random((self.shape, self.shape))
            self.lattice[self.lattice >= 0.5] = 1.0
            self.lattice[self.lattice < 0.5] = 0.0

        elif self.initial == "glider":
            self.lattice = np.zeros((self.shape, self.shape))
            start = int(self.shape / 2.0)
            self.lattice[start][start] = 1.0
            self.lattice[start + 1][start] = 1.0
            self.lattice[start - 1][start] = 1.0
            self.lattice[start + 1][start - 1] = 1.0
            self.lattice[start][start - 2] = 1.0

    def update(self) -> None:
        """Do the update following the rules"""

        nearest_neighbours = (
            np.roll(self.lattice, -1, 0)
            + np.roll(self.lattice, 1, 0)
            + np.roll(self.lattice, -1, 1)
            + np.roll(self.lattice, 1, 1)
            + np.roll(self.lattice, (1, 1), (0, 1))
            + np.roll(self.lattice, (-1, -1), (0, 1))
            + np.roll(self.lattice, (1, -1), (0, 1))
            + np.roll(self.lattice, (-1, 1), (0, 1))
        )

        # Save updates in a copy of the lattice
        new_lattice = np.copy(self.lattice)
        new_lattice[np.where((self.lattice == 0) & (nearest_neighbours == 3.0))] = 1.0
        new_lattice[np.where((self.lattice == 1) & (nearest_neighbours > 3))] = 0.0
        new_lattice[np.where((self.lattice == 1) & (nearest_neighbours < 2))] = 0.0
        self.lattice = np.copy(new_lattice)

    @property
    def total_live(self) -> float:
        """Calculate all living cells"""
        return np.sum(self.lattice)
