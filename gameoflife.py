import pygame
from pygame import draw
from pygame import Rect as rect
import pygame.freetype
import sys
import random
import copy
import argparse
import os

# Get the number of living neighbors for a cell
def neighbors(squares, i, j):
	n = 0
	if i - 1 >= 0 and j - 1 >= 0 and squares[i - 1][j - 1] :
		n += 1
	
	if j - 1 >= 0 and squares[i][j - 1]:
		n += 1
	
	if i + 1 < len(squares) and j - 1 >= 0 and squares[i + 1][j - 1]:
		n += 1
	
	if i + 1 < len(squares) and squares[i + 1][j]:
		n += 1

	if i + 1 < len(squares) and j + 1 < len(squares[0]) and squares[i + 1][j + 1]:
		n += 1
	
	if j + 1 < len(squares[0]) and squares[i][j + 1]:
		n += 1
	
	if i - 1 >= 0 and j + 1 < len(squares[0]) and squares[i - 1][j + 1]:
		n += 1

	if i - 1 >= 0 and squares[i - 1][j]:
		n += 1
	
	return n

# Process game of life rules
def process(squares):
	new_squares = copy.deepcopy(squares)
	for i in range(len(squares)):
		for j in range(len(squares[0])):
			num_neighbors = neighbors(squares, i, j)
			if squares[i][j] == True and num_neighbors != 2 and num_neighbors != 3:
				new_squares[i][j] = False
			if num_neighbors == 3 and not squares[i][j]:
				new_squares[i][j] = True
	return new_squares

# Kill all squares
def clear_squares():
	for i in range(len(squares)):
		for j in range(len(squares[0])):
			squares[i][j] = False

# Assign random living squares
def random_squares(spawn_rate):
	for i in range(len(squares)):
		for j in range(len(squares[0])):
			squares[i][j] = not bool(random.randint(0, spawn_rate))

# Export cell array to file
def export(squares, scale, width, height):
	filename = "export.txt"
	
	# Delete save file if it already exists
	try:
		os.remove(filename)
	except OSError:
		pass
	
	with open(filename, "a") as f:
		f.write("%d|%d|%d\n" % (scale, width, height))
		for j in range(len(squares)):
			for i in range(len(squares[0])):
				f.write("1" if squares[i][j] else "0")
			f.write("\n")

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--scale", type=int, help="amount of pixels to equal one cell; will impact performance (default: 20)")
parser.add_argument("--width", type=int, help="width of screen (default: 1000)")
parser.add_argument("--height", type=int, help="height of screen (default: 1000)")
parser.add_argument("--framerate", type=int, help="maximum framerate (default: 60)")
parser.add_argument("--unlimited_framerate", action="store_true", help="disable framerate limiting")
parser.add_argument("--file", help="load cells from file")
args = parser.parse_args()

scale = args.scale or 20
width = args.width or 1000
height = args.height or 1000
framerate = args.framerate or 60
unlimited_framerate = args.unlimited_framerate

pygame.init()

caption_init = "Conway's Game of Life - "
pygame.display.set_caption("Conway's Game of Life")
clock  = pygame.time.Clock()

if args.file:
	with open(args.file, "r") as f:
		file_lines = f.readlines()
	
	file_arguments = file_lines[0].split("|")
	scale = int(file_arguments[0])
	width = int(file_arguments[1])
	height = int(file_arguments[2])

	file_lines = file_lines[1:]

black = 0, 0, 0
white = 255, 255, 255
yellow = 255, 255, 0
gray = 200, 200, 200
darkgray = 50, 50, 50

# Number of cells in the x and y directions
num_x = int(width / scale)
num_y = int(height / scale)

# Game state
squares = [ [0] * num_y for _ in range(num_x)]

# Import cells if loading from file
if args.file:
	for i in range(len(file_lines)):
		for j in range(len(file_lines[0])):
			if file_lines[i][j] == "\n": continue
			squares[j][i] = bool(int(file_lines[i][j]))

# Squares for the quick save
saved_squares = [ [0] * num_y for _ in range(num_x)]

# Define the screen surface
screen = pygame.display.set_mode((width, height))

# Game variables
simulate = False
speed = 1
frame = 0
gridlines = True

# Main loop processed each frame
while True:
	frame += 1

	# Process keydown events
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		
		if event.type == pygame.KEYDOWN:
			# Play/pause
			if event.key == pygame.K_SPACE:
				simulate = not simulate
			
			# Decrease speed
			if event.key == pygame.K_LEFTBRACKET:
				speed = 2 * speed

			# Increase speed
			if event.key == pygame.K_RIGHTBRACKET:
				if speed > 1:
					speed = speed / 2
				else:
					speed = 1

			# Clear squares
			if event.key == pygame.K_c:
				clear_squares()

			# Random squares
			if event.key == pygame.K_r:
				random_squares(5)

			# Toggle gridlines
			if event.key == pygame.K_g:
				gridlines = not gridlines
			
			# Quick save
			if event.key == pygame.K_s:
				saved_squares = copy.deepcopy(squares)

			# Quick load
			if event.key == pygame.K_l:
				squares = copy.deepcopy(saved_squares)

			# Export
			if event.key == pygame.K_e:
				export(squares, scale, width, height)

			# Next frame
			if event.key == pygame.K_n:
				squares = process(squares)
			
			# Quit
			if event.key == pygame.K_ESCAPE:
				sys.exit()

	# Get current mouse position
	mouse_pos = pygame.mouse.get_pos()
	
	# Add cell when left clicked
	if pygame.mouse.get_pressed()[0]:
		i = int(mouse_pos[0] / scale)
		j = int(mouse_pos[1] / scale)
		squares[i][j] = True
	
	# Remove cell when right clicked
	if pygame.mouse.get_pressed()[2]:
		i = int(mouse_pos[0] / scale)
		j = int(mouse_pos[1] / scale)
		squares[i][j] = False
	
	screen.fill(white)

	# Draw gridlines
	if gridlines:
		for i in range(len(squares) + 1):
			draw.line(screen, gray, (i * scale, 0), (i * scale, height))
		for i in range(len(squares[0]) + 1):
			draw.line(screen, gray, (0, i * scale), (width, i * scale))

	# Draw squares
	for i in range(len(squares)):
		for j in range(len(squares[0])):
			if squares[i][j]:
				draw.rect(screen, black, rect(i * scale, j * scale, scale, scale))
	
	# Process game of life rules
	if simulate:
		if frame % speed == 0:
			squares = process(squares)

	# Update title bar with game stats
	caption = caption_init + "Speed: 1/%d, FPS: %.0f, %s" % (speed, clock.get_fps(), "Playing" if simulate else "Paused")
	pygame.display.set_caption(caption)

	# Highlight selected cell
	if not simulate:
		i = int(mouse_pos[0] / scale)
		j = int(mouse_pos[1] / scale)
		if squares[i][j]:
			draw.rect(screen, darkgray, rect(int(mouse_pos[0] / scale) * scale, int(mouse_pos[1] / scale) * scale, scale, scale))
		else:
			draw.rect(screen, gray, rect(int(mouse_pos[0] / scale) * scale, int(mouse_pos[1] / scale) * scale, scale, scale))
	
	# Limit to framerate
	if unlimited_framerate:
		clock.tick()
	else:
		clock.tick(framerate)
	
	# Render screen
	pygame.display.flip()