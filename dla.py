#!/usr/bin/env python3

import numpy
import matplotlib.pyplot as plt
import matplotlib.colors as colours
from matplotlib import colormaps as colourmaps


def create_matrix(r_max, p):
	CENTRE = r_max + p
	BOX = CENTRE * 2 + 1
	
	matrix = numpy.zeros((BOX, BOX))
	matrix[CENTRE][CENTRE] = 1
	
	y, x = numpy.ogrid[-CENTRE:CENTRE + 1, -CENTRE:CENTRE + 1]
	matrix[x ** 2 + y ** 2 >= r_max ** 2] = -1
	
	return matrix


def random_particle(r_spawn, r_max, p):
	theta = 2 * numpy.pi * numpy.random.random()
	x = int((r_spawn - 0.5) * numpy.cos(theta) + r_max + p + 0.5)
	y = int((r_spawn - 0.5) * numpy.sin(theta) + r_max + p + 0.5)

	return x, y


def calculate_radius(x, y, r_spawn, r_max, p):
	r = numpy.sqrt((x - r_max - p) ** 2 + (y - r_max - p) ** 2)
	if r + 2 > r_spawn:
		r_spawn = int(r) + 2
		if r_spawn > r_max:
			r_spawn = r_max
	print(f"Particle joined at ({x:>4}, {y:>4}), r = {r:<18}, r_spawn = {r_spawn}")

	return r_spawn


def set_colours(name, mass):
	if name in list(colourmaps):
		colourmap = colourmaps[name].resampled(mass)
		new_colourmap = colourmap(numpy.arange(1, mass + 1))
	else:
		if not name == "default":
			print("Colourmap not recognised, using default colourmap")
		new_colourmap = []
		for i in range(mass):
			new_colourmap.append(numpy.array([0, 0, 0, 1]))

	fixed = [
			colours.to_rgba('lightgray'),	#Border
			colours.to_rgba('white')		#Space
			]

	return colours.ListedColormap(numpy.concatenate((fixed, new_colourmap)))


def run(m, r_max, p):
	complete = False
	r_spawn = 2
	mass = 1

	while not complete:
		walking = True
		x, y = random_particle(r_spawn, r_max, p)
		while walking:
			if(m[x][y] == -1):#If the particle has exited the circle
				walking = False
			elif(m[x + 1][y] >= 1 or m[x - 1][y] >= 1 or m[x][y + 1] >= 1 or m[x][y - 1] >= 1):#If particle is touching the growth
				m[x][y] = mass
				mass += 1
				walking = False
				r_spawn = calculate_radius(x, y, r_spawn, r_max, p)
				if(m[x + 1][y] == -1 or m[x - 1][y] == -1 or m[x][y + 1] == -1 or m[x][y - 1] == -1):#If the growth has reached the edge of the circle
					complete = True
			else:
				x, y = [x, y] + numpy.random.choice([-1, 0, 1], size=2)

	return m, mass


def generate(r_max, p):
	m = create_matrix(r_max, p)

	return run(m, r_max, p)


if __name__ == "__main__":
	radius = 125
	padding = 5
	colourmap = "viridis"


	print(f"Generating cluster with radius = {radius} and padding = {padding}")
	cluster, mass = generate(radius, padding)
	print("Done generating!")

	import os
	print("Saving image")
	plt.matshow(cluster, cmap=set_colours(colourmap, mass))
	plt.axis('off')
	os.makedirs("out", exist_ok=True)
	path = os.path.join("out", f"dla_{radius}_{padding}_{colourmap}.png")
	plt.savefig(path, bbox_inches='tight', dpi=500)

	print("Showing cluster")
	plt.show()
