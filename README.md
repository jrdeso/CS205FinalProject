# Tower Defense

A simple tower defense game.

## Usage

```
usage: run.py [-h] [--width WIDTH] [--height HEIGHT]

Tower Defence

optional arguments:
  -h, --help       show this help message and exit
  --width WIDTH    Width of the window
  --height HEIGHT  Height of the window
```

### Game

`Q - Click` on a purple node to place a tower.
 
## Development

Install requirements using

`pip install -r requirements.txt`


Run tests from the terminal using

`ASSET_DIR=asset DATA_DIR=data python -m unittest discover -- towerd.test`

from the project directory.
