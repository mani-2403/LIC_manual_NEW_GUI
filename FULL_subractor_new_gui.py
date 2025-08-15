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

class FullSubtractorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Full Subtractor Simulation")
        self.setGeometry(100, 100, 1200, 600)
        self.setMouseTracking(True)

        # Coordinates display
        self.coord_label = QLabel(self)
        self.coord_label.setGeometry(1000, 20, 180, 30)
        self.coord_label.setStyleSheet("font-size: 14px; color: blue;")

        # Switch states: A, B, Bin
        self.switch_states = {f"switch{i+1}": False for i in range(3)}

        # Load images
        self.images = {
            "battery": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\battery.jpeg"),
            "switch_on": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\switch_on.png"),
            "switch_off": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\switch_off.png"),
            "ic_and": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\and_gate.jpeg"),
            "ic_xor": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\EXOR_gate.jpeg"),
            "ic_or": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\or_gate.jpeg"),
            "ic_not": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\not_gate.jpeg"),
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
        self.place_clickable_switch("switch3", 50, 320, 60, 60)  # Bin

        # Logic ICs for full subtractor
        self.place_image("ic_xor1", 300, 100, 160, 120)  # XOR A ^ B # XOR with Bin
        self.place_image("ic_not1", 300, 290, 160, 120)  # NOT A  # (NOT A) & B
        self.place_image("ic_and2", 600, 170, 160, 120)  # (A ⊕ B) & Bin
        self.place_image("ic_or1", 600, 350, 160, 120)   # Borrow OR

        # LEDs for outputs
        self.place_image("led_diff", 1050, 120, 60, 80)    # Difference output
        self.place_image("led_borrow", 1050, 250, 60, 80)  # Borrow output

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

            elif name.startswith("led_diff"):
                A = self.switch_states["switch1"]
                B = self.switch_states["switch2"]
                Bin = self.switch_states["switch3"]
                Diff = A ^ B ^ Bin
                pixmap = self.images["led_on"] if Diff else self.images["led_off"]

            elif name.startswith("led_borrow"):
                A = self.switch_states["switch1"]
                B = self.switch_states["switch2"]
                Bin = self.switch_states["switch3"]
                Borrow = ((not A) and B) or (((A ^ B) == 0) and Bin)  # Correct borrow logic
                pixmap = self.images["led_on"] if Borrow else self.images["led_off"]

            elif name.startswith("ic_xor1") or name.startswith("ic_xor2"):
                pixmap = self.images["ic_xor"]

            elif name.startswith("ic_and1") or name.startswith("ic_and2"):
                pixmap = self.images["ic_and"]

            elif name.startswith("ic_or1"):
                pixmap = self.images["ic_or"]

            elif name.startswith("ic_not1"):
                pixmap = self.images["ic_not"]

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

        # Wiring will follow similar style to your adder
        painter.drawLine(110,147,210,147)
        painter.drawLine(210,147,210,49)
        painter.drawLine(210,49,355,49)
        painter.drawLine(355,49,355,100)
        painter.drawLine(110,244,237,244)
        painter.drawLine(237,244,237,69)
        painter.drawLine(237,69,338,69)
        painter.drawLine(338,69,338,99)
        painter.drawLine(357,290,357,260)
        painter.drawLine(357,260,558,260)
        painter.drawLine(558,260,558,131)
        painter.drawLine(558,131,655,131)
        painter.drawLine(655,131,655,169)
        painter.drawLine(210,147,210,282)
        painter.drawLine(210,282,333,282)
        painter.drawLine(333,282,333,289)
        painter.drawLine(378,99,378,56)
        painter.drawLine(378,56,399,56)
        painter.drawLine(399,56,399,102)
        painter.drawLine(419,102,419,82)
        painter.drawLine(419,82,266,82)
        painter.drawLine(266,82,266,350)
        painter.drawLine(266,350,110,350)
        painter.drawLine(440,99,440,80)
        painter.drawLine(440,80,920,80)
        painter.drawLine(920,80,920,158)
        painter.drawLine(920,158,1056,158)
        painter.drawLine(398,60,535,60)
        painter.drawLine(535,60,535,266)
        painter.drawLine(535,266,376,266)
        painter.drawLine(376,266,376,291)
        painter.drawLine(398,291,398,272)
        painter.drawLine(398,272,564,272)
        painter.drawLine(564,272,564,308)
        painter.drawLine(564,308,616,308)
        painter.drawLine(616,308,616,290)
        painter.drawLine(266,348,266,458)
        painter.drawLine(266,458,504,458)
        painter.drawLine(504,458,504,330)
        painter.drawLine(504,330,635,330)
        painter.drawLine(635,330,635,290)
        painter.drawLine(657,290,657,338)
        painter.drawLine(657,338,582,338)
        painter.drawLine(582,338,582,497)
        painter.drawLine(582,497,638,497)
        painter.drawLine(638,497,638,470)
        painter.drawLine(236,244,564,244)
        painter.drawLine(564,244,564,149)
        painter.drawLine(564,149,634,149)
        painter.drawLine(634,149,634,169)
        painter.drawLine(658,468,658,493)
        painter.drawLine(658,493,912,493)
        painter.drawLine(912,493,912,290)
        painter.drawLine(912,290,1056,290)
        painter.drawLine(94,29,819,29)
        painter.drawLine(819,29,819,129)
        painter.drawLine(819,129,1057,129)
        painter.drawLine(1057,129,1057,498)
        painter.drawLine(1057,498,78,498)
        painter.drawLine(65,30,18,30)
        painter.drawLine(18,30,18,348)
        painter.drawLine(18,348,50,348)
        painter.drawLine(18,244,50,244)
        painter.drawLine(18,146,50,146)
        # You can extend with exact subtractor connection diagram if needed

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FullSubtractorGUI()
    win.show()
    sys.exit(app.exec())
