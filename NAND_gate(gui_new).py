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

class NandGateGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IC 7400 NAND Gate GUI")
        self.setGeometry(100, 100, 1300, 700)
        self.setMouseTracking(False)

        # Track switch states
        self.switch_states = {f"switch{i+1}": False for i in range(8)}

        # Load images
        self.images = {
            "battery": QPixmap(r"C:\Users\bhuvaneshwari\Downloads\WhatsApp Image 2025-08-06 at 12.04.41 AM.jpeg"),
            "switch_on": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\switch_on.png"),
            "switch_off": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\switch_off.png"),
            "ic_7400": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\NAND_gate.jpeg"),
            "led_on": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\led_on.png"),
            "led_off": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\led_off.png"),
            "ground": QPixmap(r"C:\Users\bhuvaneshwari\Downloads\GND.jpeg"),
        }

        self.labels = {}

        # Add components
        self.place_image("battery", 610, 10, 80, 80)
        self.place_image("ground", 610, 620, 60, 60)

        for i in range(8):
            self.place_clickable_switch(f"switch{i+1}", 50, 60 + i * 70, 60, 60)

        self.place_image("ic_7400", 500, 200, 300, 300)

        for i in range(4):
            self.place_image(f"led{i+1}", 1150, 100 + i * 100, 60, 80)

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

    def update_images(self):
        for name, label in self.labels.items():
            width = label.width()
            height = label.height()

            if name.startswith("switch"):
                pixmap = self.images["switch_on"] if self.switch_states[name] else self.images["switch_off"]
            elif name.startswith("led"):
                idx = int(name[-1])
                a = self.switch_states[f"switch{2*idx - 1}"]
                b = self.switch_states[f"switch{2*idx}"]
                # NAND logic
                output = not (a and b)
                pixmap = self.images["led_on"] if output else self.images["led_off"]
            else:
                pixmap = self.images[name]

            label.setPixmap(pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio))

    def paintEvent(self, event):
        painter = QPainter(self)
        line_pen = QPen(Qt.GlobalColor.black, 3)
        painter.setPen(line_pen)

        # Full connection lines
        painter.drawLine(110,578,690,578)
        painter.drawLine(690,578,690,502)
        painter.drawLine(110,513,650,517)
        painter.drawLine(650,517,650,500)
        painter.drawLine(110,440,465,440)
        painter.drawLine(465,440,465,528)
        painter.drawLine(465,528,567,530)
        painter.drawLine(567,530,567,501)
        painter.drawLine(113,372,420,372)
        painter.drawLine(420,372,420,550)
        painter.drawLine(420,550,529,550)
        painter.drawLine(529,550,530,501)
        painter.drawLine(450,300,110,300)
        painter.drawLine(450,300,450,186)
        painter.drawLine(450,186,688,186)
        painter.drawLine(688,186,688,200)
        painter.drawLine(110,228,428,228)
        painter.drawLine(428,228,428,169)
        painter.drawLine(428,169,725,169)
        painter.drawLine(725,169,725,199)
        painter.drawLine(110,158,610,158)
        painter.drawLine(610,158,610,200)
        painter.drawLine(110,85,565,85)
        painter.drawLine(565,85,565,198)
        painter.drawLine(609,500,609,550)
        painter.drawLine(609,550,1159,550)
        painter.drawLine(1159,550,1159,447)
        painter.drawLine(726,500,726,530)
        painter.drawLine(726,530,1120,530)
        painter.drawLine(1120,530,1120,348)
        painter.drawLine(1120,348,1155,348)
        painter.drawLine(766,199,766,186)
        painter.drawLine(766,186,1132,186)
        painter.drawLine(1132,186,1132,250)
        painter.drawLine(1132,250,1159,250)
        painter.drawLine(650,200,650,147)
        painter.drawLine(650,147,1157,147)
        painter.drawLine(670,9,1158,9)
        painter.drawLine(1158,9,1158,620)
        painter.drawLine(1158,620,640,620)
        painter.drawLine(630,9,27,9)
        painter.drawLine(27,9,27,577)
        painter.drawLine(50,577,50,514)
        painter.drawLine(25,577,50,577)
        painter.drawLine(25,510,50,510)
        painter.drawLine(25,441,50,441)
        painter.drawLine(25,373,50,373)
        painter.drawLine(25,302,50,302)
        painter.drawLine(25,228,50,228)
        painter.drawLine(25,160,50,160)
        painter.drawLine(25,84,50,84)
        painter.drawLine(530,200,530,12)
        painter.drawLine(764,500,764,619)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = NandGateGUI()
    win.show()
    sys.exit(app.exec())
