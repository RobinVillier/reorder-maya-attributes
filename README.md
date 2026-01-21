
# ReorderAttrs

A Maya tool for reordering custom attributes with an efficient UI.

<img width="302" height="531" alt="image" src="https://github.com/user-attachments/assets/ec1841de-9620-4beb-bf7d-c0901ac52a19" />

## Features

- Reorder any attributes on any Maya nodes (even locked and non keyable attributes).
- Keeps the attributes connected.
- Live connection for item selection between maya and the tool.
- User-friendly UI built with Qt.

## Project Structure

```
ReorderAttrs/
├── config/           # Configuration and settings
├── maya_logic/       # Maya attribute operations
├── ui/               # Qt-based user interface
├── resources/        # Icons and stylesheets
```

## Installation

1. Place this folder in your Maya scripts directory.
2. Run the script from Maya's Script Editor or from one fo your shelves.

## Usage

```python
from ReorderAttrs.ui import main
main.launch()
```
![reorderAttributesDemo](https://github.com/user-attachments/assets/44fca352-845c-4815-b148-b9bbe306f071)

## Requirements

- Autodesk Maya (up to 2025).
- PySide2/PyQt5.

## Contact

For issues, questions, or contributions, reach out at [rvillier99@gmail.com](mailto:rvillier99@gmail.com).
