from PyQt6.QtWidgets import QApplication, QMainWindow


from ui.StudyPlanEx import StudyPlanEx

app=QApplication([])
gui=StudyPlanEx()
gui.setupUi(QMainWindow())
gui.showWindow()
app.exec()