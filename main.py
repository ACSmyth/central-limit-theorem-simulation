import random
import sys
import time
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import matplotlib.pyplot as plt
# normal distribution visualizer

def lerp(x, a, b, c, d):
	if x < a or x > b: raise Exception(str(x) + ' not in the domain [' + str(a) + ',' + str(b) + ']')
	return (((d - c) / (b - a)) * (x - a)) + c

# generate a data point according to the given pdf and domain

def gen_cdf_vals(pdf, a, b):
	cdf_xs = []
	cdf_ys = []
	# trapezoidal approximation
	n = 1000
	inc = (b - a) / n
	s = 0

	s += pdf(a)
	cdf_xs.append(a)
	cdf_ys.append(0)
	
	x = a + inc
	while x <= b:
		pdf_val = pdf(x)
		cdf_xs.append(x)
		cdf_ys.append((s + pdf_val) * (1/2) * inc)
		s += 2 * pdf_val
		x += inc
	return [cdf_xs, cdf_ys]

def gen_cdf_and_data(pdf, a, b):
	cdf_xs, cdf_ys = gen_cdf_vals(pdf, a, b)
	return gen_data(cdf_xs, cdf_ys)

def gen_data(cdf_xs, cdf_ys):
	# gen uniform cdf and find closest y value
	ran = random.random()
	min_diff = None
	min_idx = None
	for i in range(len(cdf_ys)):
		y_val = cdf_ys[i]
		diff = abs(y_val - ran)
		if min_diff == None or diff < min_diff:
			min_diff = diff
			min_idx = i

	# return sample value
	return cdf_xs[min_idx]


w, h, = 700, 700
pygame.init()
pygame.display.set_caption('Normal Distribution')
screen = pygame.display.set_mode([w, h])

def graph(ys, trials_so_far):
	bar_width = int(w / arr_len)
	for i in range(len(ys)):
		x = lerp(i, 0, arr_len, x_min, x_max)
		y = arr_len * ys[i] / trials_so_far / 2

		# scale based on xmin/xmax
		y /= (x_max - x_min)

		if y < y_min or y > y_max: continue

		x_graph = int(lerp(x, x_min, x_max, 0, w))
		y_graph = int(lerp(y, 0, y_max, x_axis, 0))
		if x_axis - y_graph < 1: continue
		# bar graph
		pygame.draw.rect(screen, (0, 0, 0), [x_graph, y_graph, bar_width, x_axis - y_graph])

x_min = -0.2
x_max = 1
y_min = -2
y_max = 10
arr_len = 200

ys = [0 for q in range(arr_len)]
x_axis = int(lerp(0, y_min, y_max, h, 0))
y_axis = int(lerp(0, x_min, x_max, 0, w))

def pdf(x):
	return max(0, 8*x)
cdf_xs, cdf_ys = gen_cdf_vals(pdf, -0.5, 0.5)

for q in range(20000):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	avg = 0
	trials = 5
	for z in range(trials):
		avg += gen_data(cdf_xs, cdf_ys)
	avg /= trials

	if avg < x_min or avg > x_max: continue

	idx = int(lerp(avg, x_min, x_max, 0, arr_len))
	ys[idx] += 1

	screen.fill((255,255,255))

	# update graph
	graph(ys, q+1)

	# draw axes
	pygame.draw.line(screen, (0,0,0), (0, x_axis), (w, x_axis))
	pygame.draw.line(screen, (0,0,0), (y_axis, 0), (y_axis, h))

	pygame.display.flip()

pygame.quit()