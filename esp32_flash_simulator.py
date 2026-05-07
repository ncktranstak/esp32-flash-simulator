import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGroupBox, QPushButton, QLabel, 
                             QTextEdit, QComboBox, QSpinBox, QProgressBar)
from PyQt5.QtCore import Qt, QTimer, QRectF, QPointF, pyqtSignal, QThread
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPainterPath
import random
from datetime import datetime


class SimulationThread(QThread):
    """Thread for simulating flash operations"""
    progress_update = pyqtSignal(int)
    log_message = pyqtSignal(str)
    operation_complete = pyqtSignal()
    
    def __init__(self, operation, address, size):
        super().__init__()
        self.operation = operation
        self.address = address
        self.size = size
        self.running = True
    
    def run(self):
        """Simulate flash operation"""
        steps = 100
        delay_ms = 20
        
        self.log_message.emit(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Starting {self.operation} operation")
        self.log_message.emit(f"  Address: 0x{self.address:08X}, Size: {self.size} bytes")
        
        for i in range(steps + 1):
            if not self.running:
                self.log_message.emit(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Operation cancelled")
                return
            
            self.progress_update.emit(i)
            self.msleep(delay_ms)
            
            # Simulate some status messages
            if i == 25:
                self.log_message.emit(f"  SPI initialization complete")
            elif i == 50:
                self.log_message.emit(f"  Data transfer in progress...")
            elif i == 75:
                self.log_message.emit(f"  Verifying operation...")
        
        self.log_message.emit(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] {self.operation} operation completed successfully")
        self.log_message.emit(f"  Transferred: {self.size} bytes")
        self.operation_complete.emit()
    
    def stop(self):
        """Stop the simulation"""
        self.running = False


class SimulationCanvas(QWidget):
    """Canvas widget for drawing the ESP32-S3 and flash chip connection"""
    
    def __init__(self):
        super().__init__()
        self.animation_phase = 0
        self.data_flowing = False
        self.flow_direction = 0  # 0: none, 1: ESP32->Flash, 2: Flash->ESP32
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_animation)
        self.timer.start(50)  # 20 FPS
        
        self.setMinimumSize(800, 500)
    
    def start_data_flow(self, direction):
        """Start data flow animation"""
        self.data_flowing = True
        self.flow_direction = direction
    
    def stop_data_flow(self):
        """Stop data flow animation"""
        self.data_flowing = False
        self.flow_direction = 0
    
    def _update_animation(self):
        """Update animation phase"""
        if self.data_flowing:
            self.animation_phase = (self.animation_phase + 1) % 20
            self.update()
    
    def paintEvent(self, event):
        """Draw the simulation canvas"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QColor(240, 240, 245))
        
        # Define positions
        esp32_rect = QRectF(50, 150, 250, 200)
        flash_rect = QRectF(500, 150, 250, 200)
        
        # Draw ESP32-S3 SoC
        self._draw_chip(painter, esp32_rect, "ESP32-S3", QColor(70, 120, 220))
        
        # Draw Flash Chip
        self._draw_chip(painter, flash_rect, "W25Q256JWPIQ\n256Mbit NOR Flash", QColor(220, 100, 60))
        
        # Draw SPI connections
        connections = [
            ("CS", 180, QColor(255, 100, 100)),
            ("CLK", 210, QColor(100, 255, 100)),
            ("MOSI", 240, QColor(100, 200, 255)),
            ("MISO", 270, QColor(255, 255, 100)),
            ("WP", 300, QColor(200, 100, 255)),
            ("HOLD", 330, QColor(255, 150, 200)),
        ]
        
        for label, y_pos, color in connections:
            self._draw_connection(painter, esp32_rect, flash_rect, y_pos, label, color)
        
        # Draw power connections
        painter.setPen(QPen(QColor(255, 50, 50), 2))
        painter.drawLine(int(esp32_rect.right()), int(esp32_rect.top() + 30), 
                        int(flash_rect.left()), int(flash_rect.top() + 30))
        painter.setPen(QPen(QColor(50, 50, 50), 1))
        painter.drawText(QRectF(360, esp32_rect.top() + 15, 60, 20), 
                        Qt.AlignCenter, "VCC")
        
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        painter.drawLine(int(esp32_rect.right()), int(esp32_rect.bottom() - 30), 
                        int(flash_rect.left()), int(flash_rect.bottom() - 30))
        painter.setPen(QPen(QColor(50, 50, 50), 1))
        painter.drawText(QRectF(360, esp32_rect.bottom() - 35, 60, 20), 
                        Qt.AlignCenter, "GND")
        
        # Draw title
        painter.setPen(QPen(QColor(50, 50, 50), 1))
        title_font = QFont("Arial", 16, QFont.Bold)
        painter.setFont(title_font)
        painter.drawText(self.rect(), Qt.AlignTop | Qt.AlignHCenter, 
                        "ESP32-S3 ↔ SPI Flash Connection Simulator")
    
    def _draw_chip(self, painter, rect, label, color):
        """Draw a chip rectangle"""
        # Chip body
        painter.setPen(QPen(color.darker(120), 2))
        painter.setBrush(QBrush(color.lighter(140)))
        painter.drawRoundedRect(rect, 10, 10)
        
        # Chip pins (left side)
        pin_spacing = 15
        num_pins = 8
        start_y = rect.center().y() - (num_pins * pin_spacing) / 2
        for i in range(num_pins):
            pin_y = start_y + i * pin_spacing
            painter.setPen(QPen(color.darker(130), 2))
            painter.drawLine(int(rect.left() - 10), int(pin_y), int(rect.left()), int(pin_y))
        
        # Chip pins (right side)
        for i in range(num_pins):
            pin_y = start_y + i * pin_spacing
            painter.setPen(QPen(color.darker(130), 2))
            painter.drawLine(int(rect.right()), int(pin_y), int(rect.right() + 10), int(pin_y))
        
        # Label
        painter.setPen(QPen(Qt.white, 1))
        label_font = QFont("Arial", 11, QFont.Bold)
        painter.setFont(label_font)
        painter.drawText(rect, Qt.AlignCenter, label)
    
    def _draw_connection(self, painter, rect1, rect2, y_pos, label, color):
        """Draw a connection line between chips with animation"""
        start_x = rect1.right()
        end_x = rect2.left()
        
        # Base line
        painter.setPen(QPen(color, 2))
        painter.drawLine(int(start_x), int(y_pos), int(end_x), int(y_pos))
        
        # Animated data flow
        if self.data_flowing:
            dot_spacing = 20
            num_dots = 10
            
            for i in range(num_dots):
                if self.flow_direction == 1:  # ESP32 -> Flash
                    dot_x = start_x + (self.animation_phase + i * dot_spacing) % (end_x - start_x)
                elif self.flow_direction == 2:  # Flash -> ESP32
                    dot_x = end_x - (self.animation_phase + i * dot_spacing) % (end_x - start_x)
                else:
                    continue
                
                painter.setPen(QPen(color.lighter(200), 1))
                painter.setBrush(QBrush(color.lighter(180)))
                painter.drawEllipse(QPointF(dot_x, y_pos), 3, 3)
        
        # Label
        painter.setPen(QPen(QColor(50, 50, 50), 1))
        label_font = QFont("Arial", 9)
        painter.setFont(label_font)
        mid_x = (start_x + end_x) / 2
        painter.drawText(QRectF(mid_x - 30, y_pos - 20, 60, 15), 
                        Qt.AlignCenter, label)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.simulation_thread = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("ESP32-S3 Flash Simulator")
        self.setGeometry(100, 100, 1000, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Simulation canvas
        self.canvas = SimulationCanvas()
        main_layout.addWidget(self.canvas, stretch=3)
        
        # Control panel
        control_group = QGroupBox("Control Panel")
        control_layout = QHBoxLayout()
        
        # Operation selection
        op_layout = QVBoxLayout()
        op_layout.addWidget(QLabel("Operation:"))
        self.operation_combo = QComboBox()
        self.operation_combo.addItems(["Read", "Write", "Erase Sector", "Erase Block", "Chip Erase"])
        op_layout.addWidget(self.operation_combo)
        control_layout.addLayout(op_layout)
        
        # Address input
        addr_layout = QVBoxLayout()
        addr_layout.addWidget(QLabel("Address (hex):"))
        self.address_input = QSpinBox()
        self.address_input.setPrefix("0x")
        self.address_input.setDisplayIntegerBase(16)
        self.address_input.setMaximum(0x1FFFFFF)  # 32MB
        self.address_input.setValue(0x0)
        addr_layout.addWidget(self.address_input)
        control_layout.addLayout(addr_layout)
        
        # Size input
        size_layout = QVBoxLayout()
        size_layout.addWidget(QLabel("Size (bytes):"))
        self.size_input = QSpinBox()
        self.size_input.setMaximum(1024 * 1024)  # 1MB max
        self.size_input.setValue(4096)
        size_layout.addWidget(self.size_input)
        control_layout.addLayout(size_layout)
        
        # Execute button
        btn_layout = QVBoxLayout()
        btn_layout.addWidget(QLabel(""))
        self.execute_btn = QPushButton("Execute")
        self.execute_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                font-weight: bold;
            }
        """)
        self.execute_btn.clicked.connect(self._execute_operation)
        btn_layout.addWidget(self.execute_btn)
        control_layout.addLayout(btn_layout)
        
        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                text-align: center;
            }
        """)
        main_layout.addWidget(self.progress_bar)
        
        # Log panel
        log_group = QGroupBox("Operation Log")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 10pt;
            }
        """)
        self.log_text.append("ESP32-S3 Flash Simulator Ready")
        self.log_text.append("=" * 60)
        self.log_text.append("Flash Chip: Winbond W25Q256JWPIQ (256Mbit / 32MB)")
        self.log_text.append("Interface: Quad SPI (QSPI)")
        self.log_text.append("=" * 60)
        log_layout.addWidget(self.log_text)
        
        # Log controls
        log_btn_layout = QHBoxLayout()
        clear_log_btn = QPushButton("Clear Log")
        clear_log_btn.clicked.connect(self.log_text.clear)
        log_btn_layout.addWidget(clear_log_btn)
        log_btn_layout.addStretch()
        log_layout.addLayout(log_btn_layout)
        
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group, stretch=2)
        
        # Apply dark theme
        self._apply_dark_theme()
    
    def _apply_dark_theme(self):
        """Apply minimal custom styling"""
        # Use default Fusion theme colors, only customize specific elements
        pass
    
    def _execute_operation(self):
        """Execute the selected flash operation"""
        if self.simulation_thread and self.simulation_thread.isRunning():
            self.log_text.append("\n[WARNING] Operation already in progress!")
            return
        
        operation = self.operation_combo.currentText()
        address = self.address_input.value()
        size = self.size_input.value()
        
        # Disable controls during operation
        self.execute_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        
        # Start data flow animation
        if operation == "Read":
            self.canvas.start_data_flow(2)  # Flash -> ESP32
        else:
            self.canvas.start_data_flow(1)  # ESP32 -> Flash
        
        # Start simulation thread
        self.simulation_thread = SimulationThread(operation, address, size)
        self.simulation_thread.progress_update.connect(self._update_progress)
        self.simulation_thread.log_message.connect(self._add_log)
        self.simulation_thread.operation_complete.connect(self._operation_finished)
        self.simulation_thread.start()
    
    def _update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)
    
    def _add_log(self, message):
        """Add message to log"""
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def _operation_finished(self):
        """Handle operation completion"""
        self.execute_btn.setEnabled(True)
        self.canvas.stop_data_flow()
        self.log_text.append("")
    
    def closeEvent(self, event):
        """Clean up on window close"""
        if self.simulation_thread and self.simulation_thread.isRunning():
            self.simulation_thread.stop()
            self.simulation_thread.wait()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
