# Conway's Game of Life in Python
This is an implementation of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) in Python using the Pygame library.

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
* Clear all cells: c
* Randomize cells: r
* Toggle gridlines: g
* Quit: q

## Advanced Usage
Optional parameters are available on the command line:
* Help and information about parameters: `-h, --help`
* Set the scale, the amount of pixels to equal one cell; will impact performance: `--scale N`
* Set the pixel width of the screen: `--width N`
* Set the pixel height of the screen: `--height N`
* Set the framerate limit: `--framerate N`
* Remove the framerate limit `--unlimited_framerate`
* Hide all display text: `--hide_text`

## To Do
* Add import/export functionality (save width, height, and scale parameters as well)