import numpy
import matplotlib.pyplot as plt
import matplotlib.colors as colours


def create_matrix(r, s):
    box = (r + s) * 2
    matrix = numpy.zeros((box, box))
    matrix[r + s][r + s] = 1

    for x in range(box):
        for y in range(box):
            if (x - r - s) ** 2 + (y - r - s) ** 2 >= r ** 2:
                matrix[x][y] = -1

    return matrix


def random_particle(r, s):
	theta = 2 * numpy.pi * numpy.random.random()
	x = int((r - 0.5) * (numpy.cos(theta) + 1)) + s + 1
	y = int((r - 0.5) * (numpy.sin(theta) + 1)) + s + 1
	return x, y


def walk(x, y):
	rand = numpy.random.random()
	if(rand < 0.25):
		return x, y - 1
	elif(rand < 0.5):
		return x + 1, y
	elif(rand < 0.75):
		return x, y + 1
	return x - 1, y


def run(m, r, s):
	complete = False
	while not complete:
		walking = True
		x, y = random_particle(r, s)
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

if __name__ == "__main__":
	radius = 199
	space = 1
	matrix = create_matrix(radius, space)
	matrix = run(matrix, radius, space)
	plt.matshow(matrix, cmap = colours.ListedColormap(['white', 'white', 'black']))
	plt.show()
