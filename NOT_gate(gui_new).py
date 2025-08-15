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

class NotGateGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IC 7404 NOT Gate GUI with 6 Switches and 6 LEDs")
        self.setGeometry(100, 100, 1300, 700)

        # 6 switches
        self.switch_states = {f"switch{i+1}": False for i in range(6)}

        # Load images
        self.images = {
            "battery": QPixmap(r"C:\Users\bhuvaneshwari\Downloads\WhatsApp Image 2025-08-06 at 12.04.41 AM.jpeg"),
            "switch_on": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\switch_on.png"),
            "switch_off": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\switch_off.png"),
            "ic_7408": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\NOT_gate.jpeg"),
            "led_on": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\led_on.png"),
            "led_off": QPixmap(r"C:\Users\bhuvaneshwari\OneDrive\Pictures\Screenshots\component\led_off.png"),
            "ground": QPixmap(r"C:\Users\bhuvaneshwari\Downloads\GND.jpeg"),
        }

        self.labels = {}

        # Add components
        self.place_image("battery", 610, 10, 80, 80)
        self.place_image("ground", 610, 620, 60, 60)

        for i in range(6):
            self.place_clickable_switch(f"switch{i+1}", 50, 60 + i * 70, 60, 60)

        self.place_image("ic_7408", 500, 200, 300, 300)

        for i in range(6):
            self.place_image(f"led{i+1}", 1150, 60 + i * 90, 60, 80)

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
                input_state = self.switch_states.get(f"switch{idx}", False)
                pixmap = self.images["led_on"] if not input_state else self.images["led_off"]
            else:
                pixmap = self.images[name]

            label.setPixmap(pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio))

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.GlobalColor.black, 3)
        painter.setPen(pen)

        # Wiring lines
        painter.drawLine(110,437,380,437)
        painter.drawLine(380,437,380,574)
        painter.drawLine(380,574,532,574)
        painter.drawLine(532,574,531,500)
        painter.drawLine(571,500,571,555)
        painter.drawLine(571,555,1158,555)
        painter.drawLine(110,367,414,367)
        painter.drawLine(414,367,414,542)
        painter.drawLine(414,542,608,542)
        painter.drawLine(608,542,608,500)
        painter.drawLine(110,301,307,301)
        painter.drawLine(307,301,307,550)
        painter.drawLine(307,550,687,550)
        painter.drawLine(687,550,687,500)
        painter.drawLine(110,91,569,91)
        painter.drawLine(569,91,569,199)
        painter.drawLine(110,158,640,158)
        painter.drawLine(640,158,640,198)
        painter.drawLine(110,231,396,231)
        painter.drawLine(396,231,396,116)
        painter.drawLine(396,116,717,116)
        painter.drawLine(717,116,717,199)
        painter.drawLine(607,200,607,108)
        painter.drawLine(607,108,1158,108)
        painter.drawLine(686,200,686,175)
        painter.drawLine(686,175,1086,175)
        painter.drawLine(1086,175,1086,200)
        painter.drawLine(1086,200,1158,200)
        painter.drawLine(760,199,760,179)
        painter.drawLine(760,179,1020,179)
        painter.drawLine(1020,179,1020,289)
        painter.drawLine(1020,289,1158,289)
        painter.drawLine(648,500,648,534)
        painter.drawLine(648,534,1042,534)
        painter.drawLine(1042,534,1042,470)
        painter.drawLine(1042,470,1158,470)
        painter.drawLine(727,500,727,522)
        painter.drawLine(727,522,978,522)
        painter.drawLine(978,522,978,378)
        painter.drawLine(978,378,1158,378)
        painter.drawLine(629,9,18,9)
        painter.drawLine(18,9,18,437)
        painter.drawLine(18,437,50,437)
        painter.drawLine(18,371,50,371)
        painter.drawLine(18,298,50,298)
        painter.drawLine(18,230,50,230)
        painter.drawLine(18,156,50,156)
        painter.drawLine(18,88,50,88)
        painter.drawLine(666,9,1158,9)
        painter.drawLine(1158,9,1158,616)
        painter.drawLine(1158,616,635,616)
        painter.drawLine(635,616,635,619)
        painter.drawLine(766,500,766,614)
        painter.drawLine(526,200,526,9)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = NotGateGUI()
    win.show()
    sys.exit(app.exec())
