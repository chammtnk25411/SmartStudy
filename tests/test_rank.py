from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.RankEx import Rank_MainWindowEx

app=QApplication([])
myui=Rank_MainWindowEx()
myui.setupUi(QMainWindow())
myui.showWindow()
app.exec()