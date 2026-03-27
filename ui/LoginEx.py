
import json
import os
import sys
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QMainWindow
from ui.Login import Ui_MainWindow
from ui.ForgotPasswordEx import ForgotPasswordEx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from path_helper import get_path


class LoginEx(QMainWindow, Ui_MainWindow):

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        self.setupSignalAndSlot()

        self.pushButtonBack.setIcon(QIcon(get_path("images/back.jpg")))
        pixmap = QPixmap(get_path("images/book.jpg"))
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)
        icon_user = QAction(QIcon(get_path("images/login_icon.png")), "", self.MainWindow)
        self.lineEditUserName.addAction(icon_user, QLineEdit.ActionPosition.LeadingPosition)
        icon_pass = QAction(QIcon(get_path("images/lock.png")), "", self.MainWindow)
        self.lineEditPassword.addAction(icon_pass, QLineEdit.ActionPosition.LeadingPosition)

        bg = get_path("images/premain.png")
        self.MainWindow.setStyleSheet(f"""
                    QMainWindow{{
                        border-image: url({bg}) 0 0 0 0 stretch stretch;
                    }}
                """)

    def showWindow(self):
        self.MainWindow.show()
        frame = self.MainWindow.frameGeometry()
        center = self.MainWindow.screen().availableGeometry().center()
        frame.moveCenter(center)
        self.MainWindow.move(frame.topLeft())

    def setupSignalAndSlot(self):
        self.pushButtonLogin.clicked.connect(self.process_login)
        self.QuenMatKhau.mousePressEvent = self.openForgotPassword
        self.checkBoxShowPassword.stateChanged.connect(self.show_password)
        self.pushButtonBack.clicked.connect(self.back_to_premain)

    def process_login(self):
        username = self.lineEditUserName.text()
        password = self.lineEditPassword.text()

        if username == "" or password == "":
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập username và password")
            return

        from models.users import Users
        users = Users()
        user_path = get_path("datasets/user.json")
        users.import_json(user_path)

        for u in users.list:
            if u.username == username and u.password == password:
                if u.role == "admin":
                    from ui.admainEx import AdminMainWindowEx
                    self.admin_window = QMainWindow()
                    self.ui_admin = AdminMainWindowEx(username)
                    self.ui_admin.setupUi(self.admin_window)
                    self.ui_admin.showWindow()
                else:
                    from ui.MainWindowEx import MainWindowEx
                    self.main_window = QMainWindow()
                    self.ui_main = MainWindowEx(username)
                    self.ui_main.setupUi(self.main_window)
                    self.ui_main.showWindow()
                self.MainWindow.close()
                return

        QMessageBox.warning(self, "Lỗi", "Sai tài khoản hoặc mật khẩu")

    def openForgotPassword(self, event):
        self.forgot = ForgotPasswordEx()
        self.forgot.showWindow()
        self.MainWindow.hide()

    def show_password(self):
        if self.checkBoxShowPassword.isChecked():
            self.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)

    def back_to_premain(self):
        from PyQt6.QtWidgets import QMainWindow
        from ui.PreMainEx import PreMainEx

        self.premain_window = QMainWindow()
        self.ui_premain = PreMainEx()
        self.ui_premain.setupUi(self.premain_window)
        self.ui_premain.showWindow()
        self.MainWindow.close()