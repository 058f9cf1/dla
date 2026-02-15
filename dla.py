#!/usr/bin/env python3

import numpy
import matplotlib.pyplot as plt
import matplotlib.colors as colours
from matplotlib import colormaps as colourmaps


def create_matrix(centre, r_max):
    box = centre * 2 + 1

    matrix = numpy.zeros((box, box))
    matrix[centre, centre] = 1

    y, x = numpy.ogrid[-centre:centre + 1, -centre:centre + 1]
    matrix[x ** 2 + y ** 2 >= r_max ** 2] = -1

    return matrix


def spawn_particle(r_spawn, centre):
    theta = 2 * numpy.pi * numpy.random.random()
    x = int((r_spawn - 0.5) * numpy.cos(theta) + centre + 0.5)
    y = int((r_spawn - 0.5) * numpy.sin(theta) + centre + 0.5)

    return x, y


def calculate_radii(r, r_spawn, r_kill, r_max):
    if r + 1 > r_spawn and r_spawn < r_max:
        r_spawn += 1
        r_kill = r_spawn * 10

        if r_kill > r_max:
            r_kill = r_max

    return r_spawn, r_kill


def set_colours(name, mass):
    if name in list(colourmaps):
        colourmap = colourmaps[name].resampled(mass)
        new_colourmap = colourmap(numpy.arange(1, mass + 1))
    else:
        if not name == "default":
            print("Colourmap not recognised, "
                  "using default colourmap... ", end='')
            new_colourmap = []
        for i in range(mass):
            new_colourmap.append(numpy.array([0, 0, 0, 1]))

    fixed = [colours.to_rgba('lightgrey'),  # Border
             colours.to_rgba('white')]      # Space

    return colours.ListedColormap(numpy.concatenate((fixed, new_colourmap)))


def generate(r_max, p):
    complete = False
    r_spawn = 2
    r_kill = r_spawn + 1
    mass = 1

    centre = r_max + p

    m = create_matrix(centre, r_max)

    while not complete:
        walking = True
        x, y = spawn_particle(r_spawn, centre)
        while walking:
            r = numpy.linalg.norm([x - centre, y - centre])

            # If the particle has exited the circle
            if r > r_kill:
                walking = False

            # If particle is touching the growth
            elif (m[x + 1, y] >= 1 or m[x - 1, y] >= 1
                  or m[x, y + 1] >= 1 or m[x, y - 1] >= 1):
                mass += 1
                m[x, y] = mass
                walking = False
                r_spawn, r_kill = calculate_radii(r, r_spawn, r_kill, r_max)
                print(f"Particle joined at ({x:>4}, {y:>4}), "
                      f"r = {r:<18}, r_spawn = {r_spawn}, r_kill = {r_kill}, "
                      f"mass = {mass}")
                # If the growth has reached the edge of the circle
                complete = r + 1 > r_max

            # Walk
            else:
                step = 1
                if r > r_spawn:
                    step = int(r) - r_spawn + 1
                x, y = [x, y] + numpy.random.choice([-step, 0, step], size=2)

    return m, mass


if __name__ == "__main__":
    radius = 150
    padding = 1
    colourmap = "viridis"

    # Run
    print(f"Generating cluster with radius = {radius} and padding = {padding}")
    cluster, mass = generate(radius, padding)
    print("Done generating!")

    import os
    os.makedirs("out", exist_ok=True)
    path = os.path.join("out", f"dla_{radius}_{padding}_{mass}_{colourmap}")

    print("Saving array data... ", end='')
    numpy.save(f"{path}.npy", cluster)
    print("Done!")

    print("Saving image... ", end='')
    plt.matshow(cluster, cmap=set_colours(colourmap, mass))
    plt.axis('off')
    plt.savefig(f"{path}.png", bbox_inches='tight', dpi=500)
    print("Done!")

    print("Showing cluster")
    plt.show()
