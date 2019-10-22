from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFrame, \
    QSplitter, QStyleFactory, QApplication, QMessageBox, QLabel, \
    QComboBox, QLineEdit, QPushButton, QCheckBox, QSlider, QLCDNumber,\
    QPlainTextEdit, QMenuBar, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

import sys
import _io
import json
import traceback

class RedirectStream(_io.TextIOWrapper):
    def __init__(self, box):
        self.box = box

    def write(self, text):
        self.box.insertPlainText(text)

class GUI(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout(self)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter2 = QSplitter(Qt.Vertical)
        splitter3 = QSplitter(Qt.Vertical)

        splitter1.addWidget(splitter3)
        splitter1.addWidget(splitter2)

        self.console = QFrame(self)
        self.console.setFrameShape(QFrame.StyledPanel)

        self.options = QFrame(self)
        self.options.setFrameShape(QFrame.StyledPanel)

        self.map = QFrame(self)
        self.map.setFrameShape(QFrame.StyledPanel)

        self.stats = QFrame(self)
        self.stats.setFrameShape(QFrame.StyledPanel)

        splitter2.addWidget(self.console)
        splitter2.addWidget(self.options)

        splitter3.addWidget(self.map)
        splitter3.addWidget(self.stats)

        hbox.addWidget(splitter1)
        self.setLayout(hbox)

        self.console_text = QPlainTextEdit(self.console)
        self.console_text.setReadOnly(True)
        self.console_text.move(50, 50)
        self.console_text.resize(1400, 700)
        sys.stdout = RedirectStream(self.console_text)

        self.map_screen = QPlainTextEdit(self.map)
        self.map_screen.setReadOnly(True)
        self.map_screen.move(50, 50)
        self.map_screen.resize(1400, 700)

        QLabel("Health", self).move(800, 850)
        self.health = QLineEdit(self.stats)
        self.health.move(150, 150)
        self.health.setReadOnly(True)

        QLabel("Attack", self).move(850, 850)
        self.attack = QLineEdit(self.stats)
        self.attack.move(150, 150)
        self.attack.setReadOnly(True)


        self.setGeometry(300, 300, 900, 900)
        self.setWindowTitle('The Adventures of Generic Genericson')
        self.showMaximized()

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    gui = GUI()
    sys.exit(app.exec_())
