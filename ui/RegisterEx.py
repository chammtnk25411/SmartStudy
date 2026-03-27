import json
import os
import sys
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLineEdit
from ui.Register import Ui_MainWindow
from ui.LoginEx import LoginEx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from path_helper import get_path


class RegisterEx(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)

        self.ui.DangNhap.mousePressEvent = self.open_login
        self.ui.pushButtonBack.setIcon(QIcon(get_path("images/back.jpg")))
        self.ui.label_2.setPixmap(QPixmap(get_path("images/hello.png")))

        # icon
        icon_name = QtGui.QIcon(get_path("images/name.jpg"))
        self.ui.lineEditFullName.addAction(
            icon_name,
            QtWidgets.QLineEdit.ActionPosition.LeadingPosition
        )

        icon_user = QtGui.QIcon(get_path("images/login_icon.png"))
        self.ui.lineEditUserName.addAction(
            icon_user,
            QtWidgets.QLineEdit.ActionPosition.LeadingPosition
        )

        icon_email = QtGui.QIcon(get_path("images/email.jpg"))
        self.ui.lineEditEmail.addAction(
            icon_email,
            QtWidgets.QLineEdit.ActionPosition.LeadingPosition
        )

        icon_pass = QtGui.QIcon(get_path("images/lock.png"))
        self.ui.lineEditPassword.addAction(
            icon_pass,
            QtWidgets.QLineEdit.ActionPosition.LeadingPosition
        )

        self.ui.pushButtonTaoTaiKhoan.clicked.connect(self.register)
        self.ui.checkBox.stateChanged.connect(self.show_password)
        self.ui.pushButtonBack.clicked.connect(self.back_to_premain)

    def showWindow(self):
        bg = get_path("images/premain.png")
        self.setStyleSheet(f"""
                        QMainWindow{{
                            border-image: url({bg});
                        }}
                    """)
        frame = self.frameGeometry()
        center = self.screen().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())
        self.show()

    def show_password(self):
        if self.ui.checkBox.isChecked():
            self.ui.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.ui.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)

    def register(self):
        fullname = self.ui.lineEditFullName.text()
        username = self.ui.lineEditUserName.text()
        email = self.ui.lineEditEmail.text()
        password = self.ui.lineEditPassword.text()

        if fullname == "" or username == "" or email == "" or password == "":
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return

        try:
            user_path = get_path("datasets/user.json")
            with open(user_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                users = data["users"]
        except:
            users = []
            data = {"users": users}

        for user in users:
            if user["username"] == username:
                QMessageBox.warning(self, "Lỗi", "Username đã tồn tại")
                return

        if len(users) == 0:
            new_id = 1
        else:
            new_id = max(user["id"] for user in users) + 1

        new_user = {
            "id": new_id,
            "name": fullname,
            "username": username,
            "email": email,
            "password": password,
            "role": "user"
        }

        users.append(new_user)

        user_path = get_path("datasets/user.json")
        with open(user_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        QMessageBox.information(self, "Thành công", "Tạo tài khoản thành công!")

        self.ui.lineEditFullName.clear()
        self.ui.lineEditUserName.clear()
        self.ui.lineEditEmail.clear()
        self.ui.lineEditPassword.clear()

    def open_login(self, event):
        from PyQt6.QtWidgets import QMainWindow

        self.login_window = QMainWindow()
        self.ui_login = LoginEx()
        self.ui_login.setupUi(self.login_window)
        self.login_window.show()
        self.close()

    def back_to_premain(self):
        from PyQt6.QtWidgets import QMainWindow
        from ui.PreMainEx import PreMainEx

        self.premain_window = QMainWindow()
        self.ui_premain = PreMainEx()
        self.ui_premain.setupUi(self.premain_window)
        self.ui_premain.showWindow()
        self.close()