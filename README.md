# KoiBit - Simple Sprite Splitter

KoiBit is a simple, local desktop tool that cuts a sprite sheet image into a grid of smaller, individual sprites. It is built using Python and Tkinter.

## Features

* **Grid-based Splitting:** Select your sprite sheet and define the tile size (Width x Height).

* **Skip Empty Sprites:** Option to ignore completely transparent or solid-color blank tiles to save space.

* **Custom Naming:** Set a custom prefix for the output files (e.g., `player_001.png`, `player_002.png`).

* **Local & Portable:** Runs entirely on your machine. Can be built into a single `.exe` file so you don't even need Python installed.

## How to Use (Pre-built .exe)

If you just want to use the tool on Windows:

1. Go to the **Releases** tab on GitHub.

2. Download `KoiBit.exe`.

3. Run it (no installation required).

## Running from Source

If you want to run it via Python or tweak the code yourself:

### Requirements

* Python 3.x

* [Pillow](https://python-pillow.org/)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Rmate20x/KoiBit.git
   cd KoiBit
   ```

2. Install the required dependency:

   ```bash
   pip install Pillow
   ```

3. Run the script:

   ```bash
   python main.py
   ```

## Building the Executable

If you want to compile the script into a standalone `.exe` yourself:

1. Install PyInstaller:

   ```bash
   pip install pyinstaller
   ```

2. Run the following command in the project folder (ensure `icon.ico` and `pixel_operator.ttf` are in the same directory):

   ```bash
   python -m PyInstaller --onefile --windowed --add-data "pixel_operator.ttf;." --add-data "icon.ico;." --icon="icon.ico" --name="KoiBit" main.py
   ```

3. You will find the compiled `KoiBit.exe` inside the newly created `dist` folder.
