# Game_Of_Life
Conway's Game of Life in Python

Each cell uses the following rules:
1) If a cell is alive it dies if >3 or <2 nearest neighbours are alive
2) If a cell is dead it comes alive if 3 nearest neighbours are alive

Usage: Game_Of_Life.py Lattice Size, Number of Sweeps, Initial Conditions, Data/Animate

ICs: 
Random - a completely random lattice of living and dead cells
Glider - a single never ending glider 

Animate: 
Number of sweeps is irrelavent, will show the lattice indefinitely

Data: 
Random - will measure number of sweeps required to reach equilibrium 
Glider - will measure centre of mass position of a glider
