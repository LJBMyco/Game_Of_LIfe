import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
from tqdm import tqdm

from Game_Of_Life import GameOfLife


def main():

    sweeps = 1000
    shape = 250
    initial = "random"

    life = GameOfLife(shape=shape, sweeps=sweeps, initial=initial)

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
                rf"Sweeps completed: {i+1} Total living cells: {int(life.lattice.sum())}/{int(shape**2.0)}",
                horizontalalignment="center",
                verticalalignment="bottom",
                transform=ax.transAxes,
                fontsize="large",
            )
        )

        ims.append(frames)

    ani = ArtistAnimation(fig, ims)
    ani.save("GoL.gif", fps=60)


if __name__ == "__main__":
    main()
