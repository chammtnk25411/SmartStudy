from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.PreMainEx import PreMainEx

app=QApplication([])
gui=PreMainEx()
gui.setupUi(QMainWindow())
gui.showWindow()
app.exec()
