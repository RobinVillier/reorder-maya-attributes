
# ReorderAttrs

A Maya tool for reordering custom attributes with an efficient UI.

## Features

- Reorder attributes on Maya objects
- User-friendly UI built with Qt

## Project Structure

```
ReorderAttrs/
├── config/           # Configuration and settings
├── maya_logic/       # Maya attribute operations
├── ui/               # Qt-based user interface
├── resources/        # Icons and stylesheets
```

## Installation

1. Place this folder in your Maya scripts directory
2. Run the script from Maya's Script Editor or from one fo your shelves

## Usage

```python
from ReorderAttrs.ui import main
main.launch()
```

## Requirements

- Autodesk Maya (up to 2025)
- PySide2/PyQt5

## Contact

For issues, questions, or contributions, reach out at [rvillier99@gmail.com](mailto:rvillier99@gmail.com).
