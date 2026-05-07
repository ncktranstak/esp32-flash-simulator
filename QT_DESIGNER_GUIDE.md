# Qt Designer Guide

## Overview

The ESP32-S3 Flash Simulator uses a separated UI/logic architecture:

- **esp32_flash_simulator.ui** - Qt Designer UI definition (XML format)
- **main.py** - Application logic and custom widgets

This separation allows you to edit the UI visually with Qt Designer while keeping the code clean and maintainable.

## Editing the UI with Qt Designer

### Installing Qt Designer

Qt Designer is included with PyQt5 tools. Install it with:

```bash
pip install pyqt5-tools
```

On Windows, Designer is typically located at:
```
venv\Lib\site-packages\qt5_applications\Qt\bin\designer.exe
```

### Opening the UI File

```bash
# Using pyqt5-tools (if installed)
pyqt5-tools designer esp32_flash_simulator.ui

# Or directly (on Windows)
.\venv\Lib\site-packages\qt5_applications\Qt\bin\designer.exe esp32_flash_simulator.ui
```

### Editing Guidelines

1. **Don't modify canvasContainer widget** - This is a placeholder for the custom SimulationCanvas widget. It's replaced programmatically in main.py.

2. **Widget naming convention**:
   - Use camelCase for widget names
   - Names should match the Python code references in main.py

3. **Current widget names to preserve**:
   - `operationCombo` - Operation selection dropdown
   - `addressInput` - Address input spinbox
   - `sizeInput` - Size input spinbox
   - `executeBtn` - Execute button
   - `progressBar` - Progress bar
   - `logText` - Log text area
   - `clearLogBtn` - Clear log button
   - `canvasContainer` - Canvas placeholder

## Project Architecture

### main.py Structure

```python
# Custom widgets (not editable in Qt Designer)
class SimulationThread(QThread)      # Background thread for operations
class SimulationCanvas(QWidget)      # Custom drawing widget

# Main window
class MainWindow(QMainWindow)
    __init__()                       # Loads .ui file with uic.loadUi()
    _setup_canvas()                  # Adds custom SimulationCanvas
    _setup_connections()             # Connects signals/slots
    _execute_operation()             # Business logic
```

### Adding New Widgets

1. **In Qt Designer**:
   - Add the widget to the UI
   - Set a descriptive `objectName` (e.g., `myNewButton`)
   - Configure properties (text, size, etc.)
   - Save the .ui file

2. **In main.py**:
   - Access the widget via `self.myNewButton` (automatically loaded)
   - Connect signals in `_setup_connections()`:
     ```python
     self.myNewButton.clicked.connect(self._my_handler)
     ```

### Custom Widgets (Advanced)

The SimulationCanvas is a custom widget that requires manual painting. To add similar custom widgets:

1. Create a placeholder QWidget in Qt Designer
2. In Python, create your custom widget class
3. Replace the placeholder programmatically (see `_setup_canvas()`)

## Converting UI to Python (Optional)

Instead of loading .ui files at runtime, you can convert them to Python:

```bash
pyuic5 -x esp32_flash_simulator.ui -o ui_mainwindow.py
```

Then import and use in your code:
```python
from ui_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
```

**Note**: The current approach (loading .ui at runtime) is simpler for development as changes to the UI are immediately reflected without regenerating Python code.

## Testing Your Changes

After editing the UI:

1. Save the .ui file in Qt Designer
2. Run the application:
   ```bash
   python main.py
   ```
3. Test all functionality to ensure nothing broke

## Troubleshooting

### "No module named 'PyQt5.uic'"
Install PyQt5 properly:
```bash
pip install PyQt5
```

### "Failed to load ui file"
Ensure `esp32_flash_simulator.ui` is in the same directory as `main.py`.

### Widget not found error
Check that the widget's `objectName` in Qt Designer matches the name used in main.py.

### Layout issues
In Qt Designer:
- Right-click on the parent widget → Layout → Choose layout type
- Use spacers to control widget positioning
- Set size policies (Expanding, Minimum, Fixed, etc.)

## Resources

- [Qt Designer Manual](https://doc.qt.io/qt-5/qtdesigner-manual.html)
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Qt Widgets Overview](https://doc.qt.io/qt-5/widget-classes.html)
