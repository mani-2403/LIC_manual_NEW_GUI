from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QPixmap, QPainter, QPen
from PyQt6.QtCore import Qt
import sys

class ClickableLabel(QLabel):
    def __init__(self, parent=None, switch_name=""):
        super().__init__(parent)
        self.switch_name = switch_name
        self.clicked = None

    def mousePressEvent(self, event):
        if self.clicked:
            self.clicked(self.switch_name)

class BooleanFunctionGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Boolean Function: F = C’ (B’ + A’ D) + D’ B’")
        self.setGeometry(100, 100, 800, 650)  # Reduced width since no truth table

        self.switch_states = {f"switch{i+1}": False for i in range(4)}  # A, B, C, D

        self.images = {
            "battery": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\battery.jpeg"),
            "switch_on": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\switch_on.png"),
            "switch_off": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\switch_off.png"),
            "ic_7408": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\and_gate.jpeg"),
            "ic_7404": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\NOT_gate.jpeg"),
            "ic_7432": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\OR_gate.jpeg"),
            "led_on": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\led_on.png"),
            "led_off": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\led_off.png"),
            "ground": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\GND.jpeg"),
        }

        self.labels = {}

        # Power
        self.place_image("battery", 50, 10, 60, 60)
        self.place_image("ground", 50, 520, 60, 60)

        # Input switches
        for i in range(4):
            self.place_clickable_switch(f"switch{i+1}", 50, 100 + i * 80, 60, 60)

        # ICs
        self.place_image("ic_7408", 250, 70, 140, 120)  # AND
        self.place_image("ic_7404", 250, 300, 140, 120)  # NOT
        self.place_image("ic_7432", 450, 170, 140, 120)  # OR

        # LED output
        self.place_image("led", 650, 200, 60, 80)

        self.update_images()

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

    def compute_output(self, A, B, C, D):
        A_ = not A
        B_ = not B
        C_ = not C
        D_ = not D
        A_D = A_ and D
        B_or_AD = B_ or A_D
        first_term = C_ and B_or_AD
        second_term = D_ and B_
        return int(first_term or second_term)

    def update_images(self):
        for name, label in self.labels.items():
            width = label.width()
            height = label.height()

            if name.startswith("switch"):
                pixmap = self.images["switch_on"] if self.switch_states[name] else self.images["switch_off"]
            elif name == "led":
                A = self.switch_states["switch1"]
                B = self.switch_states["switch2"]
                C = self.switch_states["switch3"]
                D = self.switch_states["switch4"]
                F = self.compute_output(A, B, C, D)
                pixmap = self.images["led_on"] if F else self.images["led_off"]
            else:
                pixmap = self.images[name]

            label.setPixmap(pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio))

    def paintEvent(self, event):
        painter = QPainter(self)
        line_pen = QPen(Qt.GlobalColor.black, 3)
        painter.setPen(line_pen)
        # Circuit wiring lines (unchanged from your original)
        painter.drawLine(110,129,224,129)
        painter.drawLine(224,129,224,283)
        painter.drawLine(224,283,280,283)
        painter.drawLine(280,283,280,299)
        painter.drawLine(110,208,182,208)
        painter.drawLine(182,208,182,256)
        painter.drawLine(182,256,320,256)
        painter.drawLine(320,256,320,299)
        painter.drawLine(110,289,204,289)
        painter.drawLine(204,289,204,434)
        painter.drawLine(204,434,263,434)
        painter.drawLine(263,434,263,419)
        painter.drawLine(110,364,158,364)
        painter.drawLine(158,364,158,476)
        painter.drawLine(158,476,300,476)
        painter.drawLine(300,476,300,419)
        painter.drawLine(337,298,337,189)
        painter.drawLine(297,299,297,240)
        painter.drawLine(297,240,283,240)
        painter.drawLine(283,240,283,190)
        painter.drawLine(221,476,221,222)
        painter.drawLine(221,222,264,222)
        painter.drawLine(264,222,264,190)
        painter.drawLine(299,189,299,242)
        painter.drawLine(299,242,421,242)
        painter.drawLine(421,242,421,338)
        painter.drawLine(421,338,466,338)
        painter.drawLine(466,338,466,290)
        painter.drawLine(320,420,320,468)
        painter.drawLine(320,468,424,468)
        painter.drawLine(424,468,424,220)
        painter.drawLine(424,220,319,220)
        painter.drawLine(319,220,319,189)
        painter.drawLine(336,283,431,283)
        painter.drawLine(431,283,431,324)
        painter.drawLine(431,324,484,324)
        painter.drawLine(484,324,484,289)
        painter.drawLine(500,290,500,321)
        painter.drawLine(500,321,616,321)
        painter.drawLine(616,321,616,43)
        painter.drawLine(616,43,356,43)
        painter.drawLine(356,43,356,69)
        painter.drawLine(280,420,280,456)
        painter.drawLine(280,456,178,456)
        painter.drawLine(178,456,178,52)
        painter.drawLine(178,52,336,52)
        painter.drawLine(336,52,336,69)
        painter.drawLine(372,69,372,55)
        painter.drawLine(372,55,478,55)
        painter.drawLine(478,55,478,169)
        painter.drawLine(356,190,356,208)
        painter.drawLine(356,208,428,208)
        painter.drawLine(428,208,428,140)
        painter.drawLine(428,140,500,140)
        painter.drawLine(500,140,500,169)
        painter.drawLine(520,169,520,139)
        painter.drawLine(520,139,630,139)
        painter.drawLine(630,139,630,247)
        painter.drawLine(630,247,655,247)
        painter.drawLine(92,9,656,9)
        painter.drawLine(656,9,656,519)
        painter.drawLine(656,519,81,519)
        painter.drawLine(63,9,14,9)
        painter.drawLine(14,9,14,366)
        painter.drawLine(14,366,48,366)
        painter.drawLine(14,288,48,288)
        painter.drawLine(14,205,48,205)
        painter.drawLine(14,126,48,126)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = BooleanFunctionGUI()
    win.show()
    sys.exit(app.exec())
