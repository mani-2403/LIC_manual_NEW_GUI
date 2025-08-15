from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QPixmap, QPainter, QPen
from PyQt6.QtCore import Qt
import sys

class ClickableLabel(QLabel):
    def __init__(self, parent=None, switch_name=""):
        super().__init__(parent)
        self.switch_name = switch_name
        self.clicked = None
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        if self.clicked:
            self.clicked(self.switch_name)

class FullAdderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Full Adder Simulation")
        self.setGeometry(100, 100, 1200, 600)
        self.setMouseTracking(True)

        # Coordinates display
        self.coord_label = QLabel(self)
        self.coord_label.setGeometry(1000, 20, 180, 30)
        self.coord_label.setStyleSheet("font-size: 14px; color: blue;")

        # Switch states: A, B, Cin
        self.switch_states = {f"switch{i+1}": False for i in range(3)}

        # Load images
        self.images = {
            "battery": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\battery.jpeg"),
            "switch_on": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\switch_on.png"),
            "switch_off": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\switch_off.png"),
            "ic_and": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\and_gate.jpeg"),
            "ic_xor": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\EXOR_gate.jpeg"),
            "ic_or": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\or_gate.jpeg"),
            "led_on": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\led_on.png"),
            "led_off": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\led_off.png"),
            "ground": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\GND.jpeg"),
        }

        self.labels = {}

        # Battery & Ground
        self.place_image("battery", 50, 30, 60, 60)
        self.place_image("ground", 50, 500, 60, 60)

        # Input switches
        self.place_clickable_switch("switch1", 50, 120, 60, 60)  # A
        self.place_clickable_switch("switch2", 50, 220, 60, 60)  # B
        self.place_clickable_switch("switch3", 50, 320, 60, 60)  # Cin

        # Logic ICs for full adder
        self.place_image("ic_xor1", 300, 100, 160, 120)  # XOR for A ^ B
        self.place_image("ic_xor2", 550, 100, 1,1)  # XOR with Cin
        self.place_image("ic_and1", 300, 250, 160, 120)  # AND for A & B
        self.place_image("ic_and2", 550, 250, 1,1)  # AND for (A ^ B) & Cin
        self.place_image("ic_or1", 800, 250, 160, 120)   # OR for carry

        # LEDs for outputs
        self.place_image("led_sum", 1050, 120, 60, 80)    # Sum output
        self.place_image("led_carry", 1050, 250, 60, 80) # Carry output

        self.update_images()

    def place_image(self, name, x, y, width=60, height=60):
        lbl = QLabel(self)
        lbl.setGeometry(x, y, width, height)
        lbl.setScaledContents(True)
        lbl.setMouseTracking(True)
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
                Cin = self.switch_states["switch3"]
                Sum = A ^ B ^ Cin
                pixmap = self.images["led_on"] if Sum else self.images["led_off"]

            elif name.startswith("led_carry"):
                A = self.switch_states["switch1"]
                B = self.switch_states["switch2"]
                Cin = self.switch_states["switch3"]
                Carry = (A & B) | (B & Cin) | (A & Cin)
                pixmap = self.images["led_on"] if Carry else self.images["led_off"]

            elif name.startswith("ic_xor1") or name.startswith("ic_xor2"):
                pixmap = self.images["ic_xor"]

            elif name.startswith("ic_and1") or name.startswith("ic_and2"):
                pixmap = self.images["ic_and"]

            elif name.startswith("ic_or1"):
                pixmap = self.images["ic_or"]

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

        painter.drawLine(110,146,261,146)
        painter.drawLine(261,146,261,46)
        painter.drawLine(261,46,355,46)
        painter.drawLine(355,46,355,102)
        painter.drawLine(100,250,238,250)
        painter.drawLine(238,250,238,73)
        painter.drawLine(238,73,336,73)
        painter.drawLine(336,73,336,102)
        painter.drawLine(378,102,378,72)
        painter.drawLine(378,72,395,72)
        painter.drawLine(395,72,395,100)
        painter.drawLine(110,349,205,349)
        painter.drawLine(205,349,205,91)
        painter.drawLine(205,91,419,91)
        painter.drawLine(419,91,419,102)
        painter.drawLine(442,102,442,72)
        painter.drawLine(442,72,1058,72)
        painter.drawLine(1058,72,1058,160)
        painter.drawLine(261,146,261,409)
        painter.drawLine(261,409,314,409)
        painter.drawLine(314,409,314,370)
        painter.drawLine(238,250,238,419)
        painter.drawLine(238,419,336,419)
        painter.drawLine(336,419,336,369)
        painter.drawLine(396,86,488,86)
        painter.drawLine(488,86,488,407)
        painter.drawLine(488,407,399,407)
        painter.drawLine(399,407,399,370)
        painter.drawLine(205,349,205,446)
        painter.drawLine(205,446,379,446)
        painter.drawLine(379,446,379,370)
        painter.drawLine(421,368,421,433)
        painter.drawLine(421,433,840,433)
        painter.drawLine(840,433,840,368)
        painter.drawLine(358,370,358,421)
        painter.drawLine(358,421,815,421)
        painter.drawLine(815,421,815,369)
        painter.drawLine(856,369,856,415)
        painter.drawLine(856,415,1016,415)
        painter.drawLine(1016,415,1016,288)
        painter.drawLine(1016,288,1058,288)
        painter.drawLine(95,29,857,29)
        painter.drawLine(857,29,857,104)
        painter.drawLine(857,104,1059,104)
        painter.drawLine(1059,104,1059,499)
        painter.drawLine(1059,499,79,499)
        painter.drawLine(64,30,17,30)
        painter.drawLine(17,30,17,348)
        painter.drawLine(17,348,49,348)
        painter.drawLine(17,244,49,244)
        painter.drawLine(17,148,49,148)
        
        
        
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FullAdderGUI()
    win.show()
    sys.exit(app.exec())
