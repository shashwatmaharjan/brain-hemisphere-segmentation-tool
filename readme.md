# Brain Hemisphere Segmentation Tool

## Project Description
This Python script provides a graphical user interface (GUI) to segment the left and right hemispheres of the brain using a straight line, enabling accurate calculation of stroke areas. Additionally, the project includes a freehand line tool to demarcate any cell slices that may have merged as artifacts, ensuring proper segmentation.

## Features
- **Straight Line Segmentation:** Easily divide the brain into left and right hemispheres for precise stroke area calculation.
- **Freehand Line Tool:** Manually correct artifacts by drawing freehand lines to separate merged cell slices.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation
1. Clone the repository:
```bash
   git clone https://github.com/shashwatmaharjan/brain-hemisphere-segmentation-tool.git
   cd Brain-Hemisphere-Segmentation-Tool
   ```

2. Create the conda environment using the environment.yml file:
conda env create -f environment.yml

3. Activate the environment:
conda activate brain_hemisphere_segmentation_tool_env

## Usage

1. Run the script
```bash
python3 scripts/main.py
   ```

2. Use the GUI to segment the brain hemispheres and correct any artifacts.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
