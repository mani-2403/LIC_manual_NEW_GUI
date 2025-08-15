from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QPixmap, QPainter, QPen
from PyQt6.QtCore import Qt, QPoint
import sys

class ClickableLabel(QLabel):
    def __init__(self, parent=None, switch_name=""):
        super().__init__(parent)
        self.switch_name = switch_name
        self.clicked = None

    def mousePressEvent(self, event):
        if self.clicked:
            self.clicked(self.switch_name)

class HalfSubtractorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Half Subtractor Simulation")
        self.setGeometry(100, 100, 900, 500)
        self.setMouseTracking(True)  # Enable live mouse tracking

        # Switch states: A, B
        self.switch_states = {"A": False, "B": False}
        self.mouse_pos = QPoint(0, 0)

        # Load images
        self.images = {
            "battery": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\battery.jpeg"),
            "switch_on": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\switch_on.png"),
            "switch_off": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\switch_off.png"),
            "ic_xor": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\EXOR_gate.jpeg"),
            "ic_not": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\NOT_gate.jpeg"),
            "ic_and": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\and_gate.jpeg"),
            "led_on": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\led_on.png"),
            "led_off": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\led_off.png"),
            "ground": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\GND.jpeg"),
        }

        self.labels = {}
        self.setup_ui()
        self.update_images()

    def setup_ui(self):
        # Battery & Ground
        self.place_image("battery", 30, 30, 60, 60)
        self.place_image("ground", 30, 400, 60, 60)

        # Switches
        self.place_clickable_switch("A", 30, 120)
        self.place_clickable_switch("B", 30, 200)

        # ICs
        self.place_image("ic_xor", 300, 100, 160, 120)  # 7486 XOR
        self.place_image("ic_not", 300, 250, 160, 120) # 7404 NOT
        self.place_image("ic_and", 550, 250, 160, 120) # 7408 AND

        # LEDs
        self.place_image("led_diff", 800, 120, 60, 80)
        self.place_image("led_borrow", 800, 270, 60, 80)

    def place_image(self, name, x, y, width=60, height=60):
        lbl = QLabel(self)
        lbl.setGeometry(x, y, width, height)
        lbl.setScaledContents(True)
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
            if name in ["A", "B"]:
                pixmap = self.images["switch_on"] if self.switch_states[name] else self.images["switch_off"]
            elif name == "led_diff":
                diff = self.switch_states["A"] ^ self.switch_states["B"]
                pixmap = self.images["led_on"] if diff else self.images["led_off"]
            elif name == "led_borrow":
                borrow = (not self.switch_states["A"]) and self.switch_states["B"]
                pixmap = self.images["led_on"] if borrow else self.images["led_off"]
            else:
                pixmap = self.images.get(name, QPixmap())
            label.setPixmap(pixmap)

    def mouseMoveEvent(self, event):
        self.mouse_pos = event.pos()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # --- Circuit wiring ---
        wire_pen = QPen(Qt.GlobalColor.black, 2)
        painter.setPen(wire_pen)
        painter.drawLine(90,147,226,147)
        painter.drawLine(226,147,226,65)
        painter.drawLine(226,65,357,65)
        painter.drawLine(357,65,357,98)
        painter.drawLine(90,227,234,227)
        painter.drawLine(234,227,234,54)
        painter.drawLine(234,54,335,54)
        painter.drawLine(335,54,335,99)
        painter.drawLine(226,147,226,385)
        painter.drawLine(226,385,315,385)
        painter.drawLine(315,385,315,370)
        painter.drawLine(335,54,525,54)
        painter.drawLine(525,54,525,410)
        painter.drawLine(525,410,566,410)
        painter.drawLine(566,410,566,370)
        painter.drawLine(336,370,336,385)
        painter.drawLine(336,385,589,385)
        painter.drawLine(589,385,589,370)
        painter.drawLine(378,99,806,99)
        painter.drawLine(806,99,806,159)
        painter.drawLine(609,370,609,387)
        painter.drawLine(609,387,774,387)
        painter.drawLine(774,387,774,310)
        painter.drawLine(774,310,806,310)
        painter.drawLine(75,30,806,30)
        painter.drawLine(806,30,806,400)
        painter.drawLine(806,400,61,400)
        painter.drawLine(609,370,609,387)
        painter.drawLine(44,30,11,30)
        painter.drawLine(11,30,11,228)
        painter.drawLine(11,228,30,228)
        painter.drawLine(11,147,30,147)

        
    def setup_ui(self):
    
        # Battery & Ground
        self.place_image("battery", 30, 30, 60, 60)
        battery_text = QLabel("BATTERY", self)
        battery_text.setGeometry(20, 0, 80, 20)
        battery_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.place_image("ground", 30, 400, 60, 60)
        gnd_text = QLabel("GROUND", self)
        gnd_text.setGeometry(20, 465, 80, 20)
        gnd_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Switches
        self.place_clickable_switch("A", 30, 120)
        switch_a_text = QLabel("SWITCH A", self)
        switch_a_text.setGeometry(20, 95, 80, 20)
        switch_a_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.place_clickable_switch("B", 30, 200)
        switch_b_text = QLabel("SWITCH B", self)
        switch_b_text.setGeometry(20, 175, 80, 20)
        switch_b_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ICs (Logic Gates)
        self.place_image("ic_xor", 300, 100, 160, 120)  # XOR
        xor_text = QLabel("XOR GATE", self)
        xor_text.setGeometry(310, 80, 160, 20)
        xor_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.place_image("ic_not", 300, 250, 160, 120) # NOT
        not_text = QLabel("NOT GATE", self)
        not_text.setGeometry(310, 230, 160, 20)
        not_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.place_image("ic_and", 550, 250, 160, 120) # AND
        and_text = QLabel("AND GATE", self)
        and_text.setGeometry(550, 230, 160, 20)
        and_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # LED Labels
        lbl_diff_text = QLabel("DIFFERENCE A ⊕ B ", self)
        lbl_diff_text.setGeometry(815, 90, 100, 20)
        lbl_diff_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_borrow_text = QLabel("BORROW A'.B", self)
        lbl_borrow_text.setGeometry(800, 240, 100, 20)
        lbl_borrow_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # LEDs
        self.place_image("led_diff", 800, 120, 60, 80)
        self.place_image("led_borrow", 800, 270, 60, 80)

        
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = HalfSubtractorGUI()
    win.show()
    sys.exit(app.exec())
