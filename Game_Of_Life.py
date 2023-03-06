"""
Conway's game of life
"""

import sys
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class GameOfLife(object):
    def __init__(self, shape, sweeps, initial):

        self.shape = shape
        self.sweeps = sweeps
        self.initial = initial

        self.create_lattice()

    def create_lattice(self):
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

    ########## Update the lattice ##########

    def update(self):
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

    ########## Calculate properties of the living cells ##########

    """Calculate all living cells"""

    def total_live(self):
        return np.sum(self.lattice)

    """Find centre of mass of a glider"""

    def centre_of_mass(self):

        # Store glider positions
        X = []
        Y = []
        for i in range(self.shape):
            for j in range(self.shape):
                if self.lattice[i][j] == 1.0:
                    # If glider is at the boundary ignore
                    if (i == 0) or (i == self.shape - 1):
                        return False
                    elif (j == 0) or (j == self.shape - 1):
                        return False
                    else:
                        X.append(i)
                        Y.append(j)

        # Centre of mass is mean of living cells
        return [np.mean(X), np.mean(Y)]

    ########## Data collection ##########

    """Run model with data collection"""

    def data_collection(self):

        # Run data collection based on initial start conditions

        # If random measure time for equilibrium
        if self.inital == "random":

            t_stable = []

            # Run 200 times
            for n in range(200):
                living_cells = []
                sweeps = []
                self.create_lattice()
                for i in range(self.sweeps):
                    self.update()
                    living_cells.append(self.total_live())
                    # If three sweeps in a row have same number of living cells assume equilibrium
                    if i > 5:
                        if (
                            living_cells[i] == living_cells[i - 1]
                            and living_cells[i] == living_cells[i - 2]
                            and living_cells[i] == living_cells[i - 3]
                        ):
                            t_stable.append(i - 3)
                            break

            np.savetxt("t_stable.dat", t_stable)

        # If glider start calculate centre of mass position wrt time
        elif self.inital == "glider":

            com_position = []
            time = []
            self.create_lattice()
            for n in range(self.sweeps):
                self.update()
                # Ignore if at boundary
                if not self.centre_of_mass():
                    continue
                else:
                    com_position.append(com)
                    time.append(n)

            com_position = np.transpose(np.array(com_position))
            time = np.transpose(np.array(time))

            data = np.transpose(np.vstack(time, com_position))
            # Save data
            np.savetxt("com_data.dat", data)


if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("Incorrect Number of Arguments Presented.")
        print(
            "Usage: "
            + sys.argv[0]
            + "lattice Size, Number of sweeps, inital conditions, Data/Animate"
        )
        quit()
    elif sys.argv[3] not in ["random", "glider"]:
        print("Please choose either random IC or a glider")
        quit()
    elif sys.argv[4] not in ["data", "animate"]:
        print("Please choose either data or animate")
        quit()
    else:
        shape = int(sys.argv[1])
        sweeps = int(sys.argv[2])
        start = sys.argv[3]
        mode = sys.argv[4]

    model = GameOfLife(shape, sweeps, start)
    if mode == "data":
        model.data_collection()
