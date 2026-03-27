from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.StatisticsEx import statistics_MainWindowEx

app=QApplication([])
myui=statistics_MainWindowEx()
myui.setupUi(QMainWindow())
myui.showWindow()
app.exec()