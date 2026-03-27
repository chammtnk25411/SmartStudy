import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.timerEx import SmartStudyTimer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.chdir(os.path.join(os.path.dirname(__file__), '..', 'models'))

app = QApplication(sys.argv)
gui = SmartStudyTimer()
gui.show()
sys.exit(app.exec())