import sys
import os
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow
from ui.PreMain import Ui_MainWindow
from ui.LoginEx import LoginEx
from ui.RegisterEx import RegisterEx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from path_helper import get_path


class PreMainEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.pushButtonDangNhap.clicked.connect(self.open_login)
        self.pushButtonDangKi.clicked.connect(self.open_register)

        self.label_3.setPixmap(QPixmap(get_path("images/plan.png")))
        self.label_10.setPixmap(QPixmap(get_path("images/target.png")))
        self.label_4.setPixmap(QPixmap(get_path("images/dashboard.jpg")))
        self.label_11.setPixmap(QPixmap(get_path("images/clock.png")))

    def showWindow(self):
        self.MainWindow.show()
        bg = get_path("images/premain.png")
        self.MainWindow.setStyleSheet(f"""
                QMainWindow{{
                    border-image: url({bg});
                }}
                """)
        frame = self.MainWindow.frameGeometry()
        center = self.MainWindow.screen().availableGeometry().center()
        frame.moveCenter(center)
        self.MainWindow.move(frame.topLeft())

    def open_login(self):
        self.login_window = QMainWindow()
        self.ui_login = LoginEx()
        self.ui_login.setupUi(self.login_window)
        self.login_window.show()
        self.MainWindow.hide()

    def open_register(self):
        self.register_window = RegisterEx()
        self.register_window.showWindow()
        self.MainWindow.hide()