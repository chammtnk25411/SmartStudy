
import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.PreMainEx import PreMainEx

app = QApplication(sys.argv)
root_window = QMainWindow()
premain_ui = PreMainEx()
premain_ui.setupUi(root_window)
premain_ui.showWindow()
sys.exit(app.exec())
