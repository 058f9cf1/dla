#!/usr/bin/python

import numpy
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap as colours


def create_matrix(r, p):
	CENTRE = r + p
	BOX = CENTRE * 2 + 1
	
	matrix = numpy.zeros((BOX, BOX))
	matrix[CENTRE][CENTRE] = 1
	
	y, x = numpy.ogrid[-CENTRE:CENTRE + 1, -CENTRE:CENTRE + 1]
	matrix[x ** 2 + y ** 2 >= r ** 2] = -1
	
	return matrix


def random_particle(r, p):
	theta = 2 * numpy.pi * numpy.random.random()
	x = int((r - 0.5) * (numpy.cos(theta) + 1)) + p + 1
	y = int((r - 0.5) * (numpy.sin(theta) + 1)) + p + 1

	return x, y


def walk(x, y):
	rand = numpy.random.random()
	if(rand < 0.25):
		return x, y - 1#Up
	elif(rand < 0.5):
		return x + 1, y#Right
	elif(rand < 0.75):
		return x, y + 1#Down

	return x - 1, y#Left


def run(m, r, p):
	complete = False
	while not complete:
		walking = True
		x, y = random_particle(r, p)
		while walking:
			if(m[x][y] == -1):#If the particle has exited the circle
				walking = False
			elif(m[x + 1][y] == 1 or m[x - 1][y] == 1 or m[x][y + 1] == 1 or m[x][y - 1] == 1):#If particle has attached to the growth
				m[x][y] = 1
				walking = False
				if(m[x + 1][y] == -1 or m[x - 1][y] == -1 or m[x][y + 1] == -1 or m[x][y - 1] == -1):#If the growth has reached the edge of the circle
					complete = True
			else:
				x, y = walk(x, y)

	return m


def generate(r, p):
	m = create_matrix(r, p)

	return run(m, r, p)


if __name__ == "__main__":
	radius = 100
	padding = 5
	matrix = generate(radius, padding)
	plt.matshow(matrix, cmap = colours(['white', 'white', 'black']))
	plt.show()
