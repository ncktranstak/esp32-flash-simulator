# ESP32-S3 Flash Simulator

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A visual desktop application for simulating ESP32-S3 SoC communication with external SPI flash memory (Winbond W25Q256JWPIQ). Built with PyQt5, this tool provides an interactive interface to visualize and simulate flash operations including read, write, and erase commands.

![ESP32-S3 Flash Simulator](screenshot.png)

## Features

- 🎨 **Visual Simulation**: Real-time graphical representation of ESP32-S3 and flash chip connection
- 🔌 **SPI Interface Visualization**: Shows all SPI signal lines (CS, CLK, MOSI, MISO, WP, HOLD)
- 📊 **Data Flow Animation**: Animated data transfer visualization during operations
- 🛠️ **Operation Simulation**: Supports Read, Write, Erase Sector, Erase Block, and Chip Erase
- 📝 **Operation Log**: Detailed logging with timestamps for all operations
- ⚙️ **Configurable Parameters**: Set custom addresses and data sizes
- 🌙 **Dark Theme**: Modern dark UI for comfortable viewing

## Supported Flash Operations

- **Read**: Simulate reading data from flash memory
- **Write**: Simulate writing data to flash memory
- **Erase Sector**: Simulate erasing a 4KB sector
- **Erase Block**: Simulate erasing a 64KB block
- **Chip Erase**: Simulate erasing the entire flash chip

## Hardware Specifications

- **SoC**: ESP32-S3 (Xtensa dual-core LX7 microprocessor)
- **Flash Chip**: Winbond W25Q256JWPIQ
  - Capacity: 256Mbit (32MB)
  - Interface: Quad SPI (QSPI)
  - Voltage: 1.8V
  - Speed: Up to 133MHz

## Requirements

- Python 3.7 or higher
- PyQt5 5.15.0 or higher

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/esp32-flash-simulator.git
   cd esp32-flash-simulator
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the simulator:
```bash
python main.py
```

### Editing the UI

The application is split into two parts for easier maintenance:

1. **esp32_flash_simulator.ui** - UI layout file (can be edited with Qt Designer)
2. **main.py** - Application logic and custom widgets

To edit the UI with Qt Designer:
```bash
designer esp32_flash_simulator.ui
```

Or install Qt Designer separately if not included with PyQt5.

### How to Use

1. **Select Operation**: Choose from Read, Write, or Erase operations
2. **Set Address**: Enter the flash memory address in hexadecimal (0x000000 - 0x1FFFFFF)
3. **Set Size**: Enter the number of bytes to transfer (for Read/Write operations)
4. **Execute**: Click the "Execute" button to start the simulation
5. **Monitor**: Watch the animated data flow and check the operation log

### Keyboard Shortcuts

- Currently, all operations are mouse-driven

## Architecture

The application is structured with:
- **SimulationCanvas**: Custom widget for rendering the ESP32-S3 and flash chip visualization
- **SimulationThread**: Background thread for simulating operations without blocking the UI
- **MainWindow**: Main application window with controls and logging

## Technical Details

### SPI Signal Lines

- **CS (Chip Select)**: Active low, selects the flash chip
- **CLK (Clock)**: Serial clock signal
- **MOSI (Master Out Slave In)**: Data from ESP32-S3 to flash
- **MISO (Master In Slave Out)**: Data from flash to ESP32-S3
- **WP (Write Protect)**: Write protection control
- **HOLD**: Pauses communication without deselecting the chip

### Power Connections

- **VCC**: 1.8V power supply
- **GND**: Ground reference

## Development

### Project Structure

```
esp32-flash-simulator/
│
├── main.py                         # Main application logic
├── esp32_flash_simulator.ui        # Qt Designer UI file
├── esp32_flash_simulator.py        # Legacy single-file version (deprecated)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .gitignore                      # Git ignore rules
└── LICENSE                         # License file
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Future Enhancements

- [ ] Add support for different flash chip models
- [ ] Implement actual SPI protocol simulation
- [ ] Add power consumption monitoring
- [ ] Export operation logs to file
- [ ] Add real-time waveform display
- [ ] Support for OPI (Octal SPI) mode

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Espressif Systems for ESP32-S3 documentation
- Winbond Electronics for W25Q256 flash chip specifications
- PyQt5 community for excellent GUI framework

## Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This is a simulation tool for educational and development purposes. It does not perform actual hardware communication.
