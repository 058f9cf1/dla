#!/usr/bin/env python3

import numpy
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap as colours


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
	print(f"Particle joined at ({x:>4}, {y:>4}), r = {r:<18}, r_spawn = {r_spawn}")

	return r_spawn


def run(m, r_max, p):
	complete = False
	r_spawn = 2

	while not complete:
		walking = True
		x, y = random_particle(r_spawn, r_max, p)
		while walking:
			if(m[x][y] == -1):#If the particle has exited the circle
				walking = False
			elif(m[x + 1][y] == 1 or m[x - 1][y] == 1 or m[x][y + 1] == 1 or m[x][y - 1] == 1):#If particle is touching the growth
				m[x][y] = 1
				walking = False
				r_spawn = calculate_radius(x, y, r_spawn, r_max, p)
				if(m[x + 1][y] == -1 or m[x - 1][y] == -1 or m[x][y + 1] == -1 or m[x][y - 1] == -1):#If the growth has reached the edge of the circle
					complete = True
			else:
				x, y = [x, y] + numpy.random.choice([-1, 0, 1], size=2)

	return m


def generate(r_max, p):
	m = create_matrix(r_max, p)

	return run(m, r_max, p)


if __name__ == "__main__":
	radius = 100
	padding = 5
	print(f"Generating cluster with radius = {radius} and padding = {padding}")
	cluster = generate(radius, padding)
	print("Done! Showing cluster")
	plt.matshow(cluster, cmap = colours(['lightgray', 'white', 'black']))
	plt.axis('off')
	plt.show()
	print("Saving image")
	plt.savefig(f"dla_{radius}_{padding}.png", bbox_inches='tight')
