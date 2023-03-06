import typing as t

import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
from tqdm import tqdm
import numpy as np
import numpy.typing as npt

from Game_Of_Life import GameOfLife


def animate(life: GameOfLife, sweeps: int) -> None:
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(1, 1, 1)
    ims = []

    for i in tqdm(range(sweeps)):

        life.update()

        frames = []
        frames.append(ax.imshow(life.lattice))
        frames.append(
            ax.text(
                0.5,
                1.01,
                rf"Sweeps completed: {i+1} Total living cells: {int(life.lattice.sum())}/{int(life.shape**2.0)}",
                horizontalalignment="center",
                verticalalignment="bottom",
                transform=ax.transAxes,
                fontsize="large",
            )
        )

        ims.append(frames)

    ani = ArtistAnimation(fig, ims)
    ani.save("outputs/GoL.gif", fps=60)


def equilibrium_calculation(reruns: int, shape: int, max_sweeps: int) -> None:

    t_stable = []

    for n in tqdm(range(reruns)):
        living_cells = []
        life = GameOfLife(shape=shape, initial="random")
        equil = False
        i = 0
        while not equil and i <= max_sweeps:
            life.update()
            living_cells.append(life.total_live)
            if i > 5:
                if (
                    living_cells[i] == living_cells[i - 1]
                    and living_cells[i] == living_cells[i - 2]
                    and living_cells[i] == living_cells[i - 3]
                ):
                    t_stable.append(i - 3)
                    equil = True
            i += 1

    bins = np.linspace(0, max_sweeps, 10)
    hist, bin_edges = np.histogram(t_stable, bins)

    bin_points = np.array(
        [(b1 + b2) / 2.0 for (b1, b2) in zip(bin_edges[:-1], bin_edges[1:])]
    )

    plt.step(bin_points, hist / reruns, where="mid")
    plt.xlabel("Number of sweeps for equilibrium")
    plt.ylabel("Fraction of runs")
    plt.title(f"Time taken for {shape}x{shape} lattice to reach equilibrium")
    plt.tight_layout()
    plt.savefig("outputs/equilibrium_hist.png", dpi=500)


def mean_velocity(int_vel: npt.NDArray[np.float64]) -> float:

    for end, (i, j) in enumerate(zip(int_vel[:-1], int_vel[1:])):
        if np.sign(i) == 1 and np.sign(j) == -1:
            break

    return int_vel[0:end].mean()


def velocity(com_position: npt.NDArray[np.float64], times: npt.NDArray[np.int64]):

    int_vel = np.gradient(com_position, axis=0).T

    x_int_vel = int_vel[0]
    y_int_vel = int_vel[1]

    return mean_velocity(x_int_vel), mean_velocity(y_int_vel)


def centre_of_mass(life: GameOfLife, sweeps: int) -> None:

    times = np.arange(sweeps)
    com_position = np.zeros((sweeps, 2))

    for i, time in tqdm(enumerate(times), total=sweeps):
        life.update()
        x, y = np.where(life.lattice == 1)
        if np.all((x != 0) | (x != life.shape - 1)) and np.all(
            (x != 0) | (x != life.shape - 1)
        ):
            com_position[i][0] = np.mean(x)
            com_position[i][1] = np.mean(y)

    x_vel, y_vel = velocity(com_position, times)

    plt.plot(times, com_position.T[0], label="x")
    plt.plot(times, com_position.T[1], label="y")
    plt.title(
        f"Mean x velocity = {np.round(x_vel,2)} sites/sweep"
        f"\n Mean y velocity = {np.round(y_vel,2)} sites/sweep"
    )
    plt.xlabel("Sweep number")
    plt.ylabel("Position")
    plt.legend()
    plt.tight_layout()
    plt.savefig("outputs/centre_of_mass.png", dpi=500)


def main():

    sweeps = 1000
    shape = 250
    # initial = "random"
    initial = "glider"

    life = GameOfLife(shape=shape, initial=initial)
    # animate(life=life, sweeps=sweeps)
    # equilibrium_calculation(shape=50, reruns=200, max_sweeps=10000)
    centre_of_mass(life=life, sweeps=sweeps)


if __name__ == "__main__":
    main()
