from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QPixmap, QPainter, QPen
from PyQt6.QtCore import Qt
import sys

class ClickableLabel(QLabel):
    def __init__(self, parent=None, switch_name=""):
        super().__init__(parent)
        self.switch_name = switch_name
        self.clicked = None
        self.setMouseTracking(True)  # Enable tracking for child widgets

    def mousePressEvent(self, event):
        if self.clicked:
            self.clicked(self.switch_name)


class HalfAdderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Half Adder Simulation")
        self.setGeometry(100, 100, 1000, 500)
        self.setMouseTracking(True)  # Enable tracking for main widget

        # Label for showing coordinates
        self.coord_label = QLabel(self)
        self.coord_label.setGeometry(800, 20, 180, 30)
        self.coord_label.setStyleSheet("font-size: 14px; color: blue;")

        # Switch states: A, B
        self.switch_states = {f"switch{i+1}": False for i in range(2)}

        # Load images
        self.images = {
            "battery": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\battery.jpeg"),
            "switch_on": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\switch_on.png"),
            "switch_off": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\switch_off.png"),
            "ic_7408": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\and_gate.jpeg"),
            "ic_xor": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\EXOR_gate.jpeg"),
            "led_on": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\led_on.png"),
            "led_off": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\led_off.png"),
            "ground": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\GND.jpeg"),
        }

        self.labels = {}

        # Battery & Ground
        self.place_image("battery", 50, 30, 60, 60)
        self.place_image("ground", 50, 400, 60, 60)

        # Input switches
        self.place_clickable_switch("switch1", 50, 120, 60, 60)  # A
        self.place_clickable_switch("switch2", 50, 220, 60, 60)  # B

        # ICs for half adder: XOR & AND
        self.place_image("ic_xor", 300, 100, 160, 120)
        self.place_image("ic_7408", 300, 250, 160, 120)

        # LEDs for outputs
        self.place_image("led_sum", 600, 120, 60, 80)   # Sum output
        self.place_image("led_carry", 600, 270, 60, 80) # Carry output

        self.update_images()

    def place_image(self, name, x, y, width=60, height=60):
        lbl = QLabel(self)
        lbl.setGeometry(x, y, width, height)
        lbl.setScaledContents(True)
        lbl.setMouseTracking(True)  # Track mouse in child
        self.labels[name] = lbl

    def place_clickable_switch(self, name, x, y, width=60, height=60):
        lbl = ClickableLabel(self, switch_name=name)
        lbl.setGeometry(x, y, width, height)
        lbl.setScaledContents(True)
        lbl.clicked = self.toggle_switch
        self.labels[name] = lbl

    def toggle_switch(self, name):
        self.switch_states[name] = not self.switch_states[name]
        self.update_images()
        self.update()

    def update_images(self):
        for name, label in self.labels.items():
            w, h = label.width(), label.height()

            if name.startswith("switch"):
                pixmap = self.images["switch_on"] if self.switch_states[name] else self.images["switch_off"]

            elif name.startswith("led_sum"):
                A = self.switch_states["switch1"]
                B = self.switch_states["switch2"]
                Sum = A ^ B
                pixmap = self.images["led_on"] if Sum else self.images["led_off"]

            elif name.startswith("led_carry"):
                A = self.switch_states["switch1"]
                B = self.switch_states["switch2"]
                Carry = A & B
                pixmap = self.images["led_on"] if Carry else self.images["led_off"]

            else:
                pixmap = self.images[name]

            label.setPixmap(pixmap.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio))

    def mouseMoveEvent(self, event):
        x, y = event.position().x(), event.position().y()
        self.coord_label.setText(f"X: {int(x)}, Y: {int(y)}")
        super().mouseMoveEvent(event)
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(Qt.GlobalColor.black, 3)
        painter.setPen(pen)

        painter.drawLine(108,145,200,145)
        painter.drawLine(200,145,200,63)
        painter.drawLine(200,63,356,63)
        painter.drawLine(356,63,356,103)
        painter.drawLine(108,246,229,246)
        painter.drawLine(229,246,229,76)
        painter.drawLine(229,76,338,76)
        painter.drawLine(338,76,338,104)
        painter.drawLine(200,145,200,395)
        painter.drawLine(200,395,336,395)
        painter.drawLine(336,395,336,368)
        painter.drawLine(229,240,229,392)
        painter.drawLine(229,392,319,392)
        painter.drawLine(319,392,319,367)
        painter.drawLine(376,100,376,65)
        painter.drawLine(376,65,603,65)
        painter.drawLine(603,65,603,158)
        painter.drawLine(362,370,362,393)
        painter.drawLine(362,393,539,393)
        painter.drawLine(539,393,539,283)
        painter.drawLine(539,283,603,283)
        painter.drawLine(603,283,603,307)
        painter.drawLine(95,28,605,28)
        painter.drawLine(605,28,605,397)
        painter.drawLine(605,397,80,397)
        painter.drawLine(66,28,22,28)
        painter.drawLine(22,28,22,248)
        painter.drawLine(22,248,50,248)
        painter.drawLine(22,148,50,148)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = HalfAdderGUI()
    win.show()
    sys.exit(app.exec())
