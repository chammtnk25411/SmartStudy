import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem, QMessageBox
from PyQt6.QtCore import pyqtSignal
from ui.Motivation import Ui_MainWindow
from models.motivation import Motivation
from models.motivations import Motivations

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from path_helper import get_path


class MotivationEx(QMainWindow, Ui_MainWindow):
    data_changed = pyqtSignal()

    def __init__(self, username):
        super().__init__()
        self.current_username = username
        self.setupUi(self)

        self.pushButtonNew.setIcon(QIcon(get_path("images/ic_add.png")))
        self.pushButtonSave.setIcon(QIcon(get_path("images/ic_save.png")))
        self.pushButtonDelete.setIcon(QIcon(get_path("images/ic_delete.png")))
        self.pushButtonBack.setIcon(QIcon(get_path("images/back.jpg")))

        self.motivations = Motivations()
        self.json_path = get_path("datasets/motivations.json")

        if os.path.exists(self.json_path):
            self.motivations.import_json(self.json_path)
        self.showMotivations()

        self.pushButtonNew.clicked.connect(self.processNew)
        self.pushButtonSave.clicked.connect(self.processSave)
        self.pushButtonDelete.clicked.connect(self.processDelete)
        self.pushButtonBack.clicked.connect(self.processBack)

        self.listWidgetMotivation.itemSelectionChanged.connect(self.processItemSelectionChanged)

        bg = get_path("images/nen.png")
        self.setStyleSheet(f"""
                        QMainWindow{{
                            border-image: url({bg});
                        }}
                        """)

    def showMotivations(self):
        self.listWidgetMotivation.clear()
        user_motivations = self.motivations.get_by_username(self.current_username)
        for m in user_motivations:
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, m)
            item.setText(m.Content)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.listWidgetMotivation.addItem(item)

    def processNew(self):
        self.lineEditId.clear()
        self.lineEditContent.clear()
        self.lineEditId.setFocus()

    def processSave(self):
        id_val = self.lineEditId.text().strip()
        content_val = self.lineEditContent.text().strip()

        if id_val == "" or content_val == "":
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập dữ liệu")
            return

        m = Motivation(id_val, content_val, self.current_username)
        self.motivations.save_item(m)
        self.showMotivations()
        self.data_changed.emit()

    def processItemSelectionChanged(self):
        row = self.listWidgetMotivation.currentRow()
        if row < 0:
            return
        item = self.listWidgetMotivation.item(row)
        m = item.data(Qt.ItemDataRole.UserRole)
        self.lineEditId.setText(m.Id)
        self.lineEditContent.setText(m.Content)

    def processDelete(self):
        reply = QMessageBox.question(
            self,
            "Xác nhận",
            "Bạn có chắc muốn xoá?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            return

        for i in range(self.listWidgetMotivation.count() - 1, -1, -1):
            item = self.listWidgetMotivation.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                m = item.data(Qt.ItemDataRole.UserRole)
                self.motivations.remove_item(m.Id)

        self.showMotivations()
        self.data_changed.emit()

    def processBack(self):
        if hasattr(self, 'main_window_ref') and self.main_window_ref:
            self.main_window_ref.show()
        self.close()