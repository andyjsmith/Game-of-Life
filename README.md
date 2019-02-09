# Conway's Game of Life in Python
This is an implementation of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) in Python using the Pygame library.


![Preview](/preview.gif?raw=true)

## Requirements
* Python 3
* Pygame: `pip install pygame`

Will not work in a headless environment.

## Usage
`python gameoflife.py`

Controls:
* Run the simulation: space
* Add cell: left click
* Remove cell: right click
* Decrease simulation speed: left bracket "["
* Increase simulation speed: right bracket "]"
* Next frame (run simulation for one frame, when paused): N
* Clear all cells: C
* Randomize cells: R
* Quick save: S
* Quick load: L
* Toggle gridlines: G
* Quit: Q

## Command-Line Parameters
Optional parameters are available on the command line:
* Help and information about parameters: `-h, --help`
* Set the scale, the amount of pixels to equal one cell; will impact performance: `--scale N`
* Set the width and height based on the number of pixels: `--window WIDTHxHEIGHT`
* Set the width and height based on the number of cells you want: `--size XCELLSxYCELLS`
* Set the framerate limit: `--framerate N`
* Remove the framerate limit `--unlimited_framerate`
* Load an exported cell file: `--file FILE.txt`