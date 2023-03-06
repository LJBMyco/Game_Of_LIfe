import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
from tqdm import tqdm
import numpy as np

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


def main():

    sweeps = 1000
    shape = 250
    initial = "random"

    # life = GameOfLife(shape=shape, initial=initial)
    # animate(life=life, sweeps=sweeps)
    equilibrium_calculation(shape=50, reruns=200, max_sweeps=10000)


if __name__ == "__main__":
    main()
